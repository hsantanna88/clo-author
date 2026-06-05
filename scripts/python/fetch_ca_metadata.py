"""
fetch_ca_metadata.py
--------------------
Queries the Library of Congress item JSON API for each LCCN in
data/chronicling-america-meta.xlsx and writes enriched metadata
(including partisan affiliation from the 'note' field) to
data/ca_title_metadata.csv.

LOC rate limits (no API key exists):
  Burst:  20 req / 1 min  → 5-min block if exceeded
  Crawl:  20 req / 10 sec → 1-hr  block if exceeded
  Safe rate: 1 request every 3.5 s ≈ 17 req/min

Checkpoint/resume: already-fetched LCCNs are skipped on restart,
so it's safe to Ctrl-C and rerun if you hit a long block.

Run from repo root:
    python scripts/fetch_ca_metadata.py

Requires: pandas, openpyxl, curl_cffi  (pip install curl_cffi)
"""

import random
import re
import sys
import time
from html.parser import HTMLParser

import pandas as pd
from curl_cffi import requests

# ── Config ────────────────────────────────────────────────────────────────────
META_XLSX   = "data/chronicling-america-meta.xlsx"
OUT_CSV     = "data/ca_title_metadata.csv"
BASE_URL    = "https://www.loc.gov/item/{lccn}/?fo=json&at=item"
DELAY_SEC   = 3.5   # 17 req/min — safely under the 20/min burst limit
TIMEOUT_SEC = 20

# On 429 the LOC issues a 5-min (burst) or 1-hr (crawl) block.
# We wait progressively: 5 min → 10 min → 65 min → give up.
BACKOFF_SCHEDULE = [5 * 60, 10 * 60, 65 * 60]

# ── Partisan classifier ───────────────────────────────────────────────────────
# Applied to the raw 'notes' text concatenated from all note entries.
# Order matters: check specific phrases before generic ones.
PARTISAN_PATTERNS = [
    # Independent-leaning variants first (most specific)
    (r"\bindependent\s+republican\b",       "Independent Republican"),
    (r"\bindependent\s+democrat\b",         "Independent Democrat"),
    (r"\bundependent\b",                    "Independent"),          # typo seen in CA data
    (r"\bindependent\b",                    "Independent"),
    # Core partisan labels
    (r"\brepublican\b",                     "Republican"),
    (r"\bdemocrat(?:ic)?\b",               "Democratic"),
    (r"\bwhig\b",                           "Whig"),
    (r"\bunion(?:ist)?\b",                  "Unionist"),
    (r"\bneutral\b",                        "Neutral"),
    (r"\bnon.?partisan\b",                  "Nonpartisan"),
]

def _strip_html(html: str) -> str:
    """Remove HTML tags and decode entities, returning plain text."""
    class _P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.parts = []
        def handle_data(self, data):
            self.parts.append(data)
    p = _P()
    p.feed(html or "")
    return " ".join(p.parts).strip()


def classify_partisan(notes_text: str) -> str:
    """Return best-guess partisan label from concatenated note strings."""
    t = notes_text.lower()
    for pattern, label in PARTISAN_PATTERNS:
        if re.search(pattern, t):
            return label
    return ""   # blank = not stated / not parseable


# ── Helpers ───────────────────────────────────────────────────────────────────
def _coerce_list(val) -> list:
    """Normalise a field that may be a string, list, or None to a list."""
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def _is_captcha(response: requests.Response) -> bool:
    """Return True if LOC returned an HTML CAPTCHA page instead of JSON."""
    ct = response.headers.get("Content-Type", "")
    return "text/html" in ct


# ── API fetch ─────────────────────────────────────────────────────────────────
def fetch_title(lccn: str, session: requests.Session) -> dict:
    """Fetch one LCCN from the LOC item API; return parsed dict."""
    url = BASE_URL.format(lccn=lccn.strip())

    for attempt, backoff in enumerate(BACKOFF_SCHEDULE + [None]):
        try:
            r = session.get(url, timeout=TIMEOUT_SEC, impersonate="edge101")
        except Exception as e:
            return {"lccn": lccn, "api_status": f"connection_error: {e}"}

        if r.status_code == 404:
            return {"lccn": lccn, "api_status": "404_not_found"}

        # Rate-limited or CAPTCHA
        if r.status_code == 429 or _is_captcha(r):
            if backoff is None:
                print(f"    ✗ {lccn}: still blocked after all retries — skipping")
                return {"lccn": lccn, "api_status": "429_blocked"}
            mins = backoff // 60
            print(f"    ⚠ Rate limited (attempt {attempt+1}) — waiting {mins} min...",
                  flush=True)
            time.sleep(backoff)
            continue

        if not r.ok:
            return {"lccn": lccn, "api_status": f"http_{r.status_code}"}

        # Check we actually got JSON (not a surprise HTML page)
        if _is_captcha(r):
            continue

        try:
            payload = r.json()
        except Exception as e:
            return {"lccn": lccn, "api_status": f"json_parse_error: {e}"}

        break  # success

    # With ?at=item the fields are at the top level; fall back to "item" wrapper
    # for any responses that still use the nested form.
    data = payload if "title" in payload else payload.get("item", payload)

    notes        = _coerce_list(data.get("notes") or data.get("note"))
    notes_concat = " | ".join(str(n) for n in notes if n)

    essay_html  = data.get("essay", "") or ""
    essay_text  = _strip_html(essay_html) if essay_html else ""

    # Combine notes + essay so partisan classifier sees both sources
    combined_for_classification = " | ".join(filter(None, [notes_concat, essay_text]))

    raw_subjects = _coerce_list(data.get("subject") or data.get("subject_headings"))
    subjects = [
        s.get("name", str(s)) if isinstance(s, dict) else str(s)
        for s in raw_subjects
    ]

    locations    = _coerce_list(data.get("location") or data.get("place"))
    location_str = "; ".join(str(l) for l in locations if l)

    publisher_raw = data.get("publisher", "")
    publisher = "; ".join(_coerce_list(publisher_raw)) if isinstance(publisher_raw, list) \
                else str(publisher_raw or "")

    dates_raw = _coerce_list(data.get("dates", []))

    return {
        "lccn":           lccn,
        "api_status":     "ok",
        "title":          data.get("title", ""),
        "publisher":      publisher,
        "place_of_pub":   data.get("place_of_publication", location_str),
        "location":       location_str,
        "date":           data.get("date", ""),
        "dates":          "; ".join(str(d) for d in dates_raw),
        "language":       "; ".join(_coerce_list(data.get("language"))),
        "subjects":       "; ".join(subjects),
        "notes_raw":      notes_concat,
        "essay_text":     essay_text,
        "partisan_label": classify_partisan(combined_for_classification),
    }


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    # ── Load LCCNs ───────────────────────────────────────────────────────────
    meta = pd.read_excel(META_XLSX)
    lccn_col = next(
        (c for c in meta.columns if c.strip().upper() == "LCCN"), None
    )
    if lccn_col is None:
        raise ValueError(f"No LCCN column found. Columns: {meta.columns.tolist()}")

    all_lccns = meta[lccn_col].dropna().astype(str).str.strip().unique().tolist()

    # ── Checkpoint: skip LCCNs already written to the output CSV ─────────────
    try:
        existing = pd.read_csv(OUT_CSV, usecols=["lccn"], dtype=str)
        done = set(existing["lccn"].str.strip())
        print(f"Resuming — {len(done)} LCCNs already fetched, {len(all_lccns)-len(done)} remaining.")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        done = set()
        print(f"Starting fresh — {len(all_lccns)} LCCNs to fetch.")

    todo = [l for l in all_lccns if l not in done]
    if not todo:
        print("Nothing to do — all LCCNs already fetched.")
        return

    # curl_cffi impersonates Edge's TLS fingerprint + headers automatically
    session = requests.Session(impersonate="edge101")
    # Warm the session to pick up any LOC cookies
    try:
        session.get("https://www.loc.gov/", timeout=TIMEOUT_SEC)
        time.sleep(2)
    except Exception:
        pass

    # Open CSV in append mode so each row is saved immediately
    write_header = not done  # only write header on first run
    total        = len(all_lccns)
    fetched_so_far = len(done)

    with open(OUT_CSV, "a", newline="", encoding="utf-8") as f:
        for i, lccn in enumerate(todo, 1):
            row = fetch_title(lccn, session)
            fetched_so_far += 1

            partisan = row.get("partisan_label", "")
            status   = row.get("api_status", "")
            title    = row.get("title", "")[:45]
            print(
                f"  [{fetched_so_far:>4}/{total}]  {lccn:<20}  "
                f"{status:<20}  {partisan:<25}  {title}",
                flush=True,
            )

            # Write row to CSV immediately (survives Ctrl-C mid-run)
            row_df = pd.DataFrame([row])
            row_df.to_csv(f, header=write_header, index=False)
            write_header = False  # only write header once

            # Don't sleep after the last item; jitter avoids robotic cadence
            if i < len(todo):
                time.sleep(DELAY_SEC + random.uniform(0, 1.5))

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\nDone. Results in {OUT_CSV}")
    out = pd.read_csv(OUT_CSV, dtype=str)
    ok  = out[out["api_status"] == "ok"]

    print(f"\nPartisan label coverage: "
          f"{(ok['partisan_label'] != '').sum()}/{len(ok)} successfully fetched titles")
    print("\nLabel distribution:")
    print(ok["partisan_label"].replace("", "(not stated)").value_counts().to_string())

    unlabeled = ok[ok["partisan_label"] == ""]
    if not unlabeled.empty:
        print(f"\nUnlabeled titles — inspect 'notes_raw' / 'essay_text' for manual coding:")
        for _, r in unlabeled.head(20).iterrows():
            has_essay = "essay" if str(r.get("essay_text", "")).strip() else "     "
            print(f"  {r['lccn']:<20}  {str(r['title'])[:40]:<42}  "
                  f"[{has_essay}]  notes: {str(r.get('notes_raw',''))[:60]}")


if __name__ == "__main__":
    main()
