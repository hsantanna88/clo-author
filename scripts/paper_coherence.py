#!/usr/bin/env python3
"""
paper_coherence.py — deterministic coherence engine for LaTeX papers.

Builds an index of a paper's cross-reference, citation, and numeric structure,
then runs checks that have a right answer. Every finding it emits is verifiable
without trusting a language model: a reference either resolves or it does not, a
number either appears in the cited table or it does not.

Judgment calls are deliberately out of scope. This is the verifier, not the
referee. The reasoning layer that sits on top of this (see the /coherence skill)
consumes the JSON index and handles only what parsing cannot reach.

Standard library only. Python 3.9+.

Usage:
    python3 scripts/paper_coherence.py [--paper DIR] [--main FILE]
                                       [--json OUT.json] [--markdown OUT.md]
                                       [--scope FILE] [--min-severity LEVEL]
                                       [--fix] [--quiet]

Exit codes:
    0  no blocking findings
    1  at least one blocking (major) finding
    2  engine error (bad paths, unparseable main file)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

VERSION = "1.0.0"

# Severity ordering. `major` findings are blocking; `minor` and `info` are not.
SEVERITY_ORDER = {"major": 0, "minor": 1, "info": 2}
BLOCKING = {"major"}


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------


@dataclass
class Finding:
    check: str
    severity: str
    file: str
    line: int
    message: str
    evidence: str = ""
    suggestion: str = ""
    autofix: bool = False

    def sort_key(self) -> Tuple[int, str, int]:
        return (SEVERITY_ORDER.get(self.severity, 9), self.file, self.line)

    def to_dict(self) -> dict:
        return {
            "check": self.check,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "message": self.message,
            "evidence": self.evidence,
            "suggestion": self.suggestion,
            "autofix": self.autofix,
        }


@dataclass
class Located:
    """Anything with a source position."""

    value: str
    file: str
    line: int


@dataclass
class ProseNumber:
    """A numeric literal appearing in prose, with what the surrounding text says it is."""

    raw: str
    value: float
    kind: str  # estimate | se | pvalue | stat | derived | count
    file: str
    line: int
    context: str


@dataclass
class TableNumber:
    """A numeric cell in a tabular body."""

    raw: str
    value: float
    kind: str  # point | se | count
    row_label: str
    col: int
    panel: str
    stars: int


@dataclass
class TableDoc:
    path: str
    numbers: List[TableNumber] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    wrapped: bool = False  # contains \begin{table} or \caption — violates INV-13


@dataclass
class EnvBlock:
    """A displayed-math or theorem-like environment body."""

    env: str
    label: str
    body: str
    file: str
    line: int
    symbols: List[str] = field(default_factory=list)


@dataclass
class Paragraph:
    text: str
    file: str
    line: int
    zone: str  # abstract | body
    section: str = ""  # nearest preceding (sub)section heading
    refs: List[str] = field(default_factory=list)
    numbers: List[ProseNumber] = field(default_factory=list)


# --------------------------------------------------------------------------
# TeX source handling
# --------------------------------------------------------------------------

COMMENT_RE = re.compile(r"(?<!\\)%.*$")

# Float environments whose bodies are not prose claims (their notes are full of
# threshold numbers like $p<0.05$ that would otherwise read as claims).
FLOAT_ENVS = {"table", "table*", "figure", "figure*", "sidewaystable", "landscape"}

# Displayed math and theorem-like environments. Their bodies are the candidate
# spans the reasoning layer reads — the specification auditor needs equations,
# the theory auditor needs proofs, the notation auditor needs symbols.
MATH_ENVS = {"equation", "align", "gather", "multline", "eqnarray"}
THEORY_ENVS = {
    "theorem",
    "proposition",
    "lemma",
    "corollary",
    "definition",
    "assumption",
    "proof",
    "hyp",
}

# Single-letter Latin/Greek math symbols, with optional sub/superscripts stripped.
SYMBOL_RE = re.compile(r"\\([a-zA-Z]{2,})\b|(?<![\\a-zA-Z])([a-zA-Z])(?![a-zA-Z])")
SYMBOL_STOPWORDS = {
    "begin", "end", "label", "frac", "text", "left", "right", "sum", "prod", "int",
    "cdot", "times", "quad", "qquad", "mathbb", "mathcal", "mathrm", "hat", "bar",
    "tilde", "widehat", "operatorname", "log", "exp", "min", "max", "sqrt", "partial",
    "in", "geq", "leq", "neq", "approx", "sim", "big", "Big", "nonumber", "notag",
}

# Length units — a number followed by one of these is a layout dimension.
UNIT_RE = re.compile(
    r"^\s*(pt|pc|in|bp|cm|mm|dd|cc|sp|ex|em|mu|\\textwidth|\\linewidth|\\columnwidth|\\textheight)"
)


def strip_comments(line: str) -> str:
    return COMMENT_RE.sub("", line)


def normalize_ws(text: str) -> str:
    """LaTeX nonbreaking spaces and line breaks behave as whitespace for our purposes."""
    return re.sub(r"[~\s]+", " ", text).strip()


class Source:
    """One .tex file, comment-stripped, with 1-indexed line access."""

    def __init__(self, path: Path, root: Path):
        self.path = path
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            raw = ""
        self.rel = os.path.relpath(path, root)
        self.lines = [strip_comments(ln) for ln in raw.splitlines()]
        self.text = "\n".join(self.lines)

    def line_of(self, offset: int) -> int:
        return self.text.count("\n", 0, offset) + 1


# --------------------------------------------------------------------------
# Index
# --------------------------------------------------------------------------

LABEL_RE = re.compile(r"\\label\s*\{([^}]*)\}")
REF_RE = re.compile(r"\\(?:c|C|auto|page|eq|v|f)?ref\s*\*?\s*\{([^}]*)\}")
CITE_RE = re.compile(
    r"\\(?:no)?(?:text|paren|foot|auto|super|smart|full)?cite[a-zA-Z]*\s*"
    r"(?:\[[^\]]*\]\s*)*\{([^}]*)\}"
)
INPUT_RE = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]*)\}")
GRAPHIC_RE = re.compile(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}")
BEGIN_RE = re.compile(r"\\begin\s*\{([^}]*)\}")
END_RE = re.compile(r"\\end\s*\{([^}]*)\}")
NEWCMD_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand|DeclareMathOperator)\s*\*?\s*"
    r"\{?\\([a-zA-Z@]+)\}?"
)
SECTION_RE = re.compile(r"\\(sub)*section\s*\*?\s*\{")
BIBKEY_RE = re.compile(r"^\s*@[a-zA-Z]+\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)
BIBRESOURCE_RE = re.compile(r"\\(?:addbibresource|bibliography)\s*\{([^}]*)\}")


class Index:
    def __init__(self, root: Path, main: Path):
        self.root = root
        self.main = main
        self.sources: Dict[str, Source] = {}
        self.labels: Dict[str, List[Located]] = {}
        self.refs: List[Located] = []
        self.cites: List[Located] = []
        self.bibkeys: Set[str] = set()
        self.bibfiles: List[str] = []
        self.inputs: List[Located] = []
        self.graphics: List[Located] = []
        self.commands: Dict[str, List[Located]] = {}
        self.tables: Dict[str, TableDoc] = {}  # rel path -> TableDoc
        self.label_to_table: Dict[str, str] = {}  # label -> table rel path
        self.label_kind: Dict[str, str] = {}  # label -> table | figure | equation | section
        self.float_context: Dict[str, dict] = {}  # label -> {caption, notes}
        self.paragraphs: List[Paragraph] = []
        self.environments: List[EnvBlock] = []
        self.missing_inputs: List[Located] = []

    # -- traversal ---------------------------------------------------------

    def build(self) -> None:
        self._walk(self.main, seen=set())
        self._load_bib()
        self._load_tables()

    def _resolve_input(self, target: str, origin: Path) -> Optional[Path]:
        target = target.strip()
        if not target:
            return None
        candidates = []
        for base in (origin.parent, self.root, self.main.parent):
            for suffix in ("", ".tex"):
                candidates.append(base / (target + suffix))
        for cand in candidates:
            if cand.is_file():
                return cand
        return None

    def _walk(self, path: Path, seen: Set[Path]) -> None:
        rp = path.resolve()
        if rp in seen or not path.is_file():
            return
        seen.add(rp)
        src = Source(path, self.root)
        self.sources[src.rel] = src
        self._scan(src)
        for m in INPUT_RE.finditer(src.text):
            target = m.group(1).strip()
            line = src.line_of(m.start())
            resolved = self._resolve_input(target, path)
            loc = Located(target, src.rel, line)
            self.inputs.append(loc)
            if resolved is None:
                self.missing_inputs.append(loc)
                continue
            # Table bodies are parsed separately, not walked as prose.
            if "tables/" in target or resolved.parent.name == "tables":
                self.tables.setdefault(
                    os.path.relpath(resolved, self.root), TableDoc(os.path.relpath(resolved, self.root))
                )
                continue
            self._walk(resolved, seen)

    # -- per-file scanning -------------------------------------------------

    def _scan(self, src: Source) -> None:
        for m in LABEL_RE.finditer(src.text):
            key = m.group(1).strip()
            self.labels.setdefault(key, []).append(Located(key, src.rel, src.line_of(m.start())))
        for m in REF_RE.finditer(src.text):
            for key in m.group(1).split(","):
                key = key.strip()
                if key:
                    self.refs.append(Located(key, src.rel, src.line_of(m.start())))
        for m in CITE_RE.finditer(src.text):
            for key in m.group(1).split(","):
                key = key.strip()
                if key:
                    self.cites.append(Located(key, src.rel, src.line_of(m.start())))
        for m in GRAPHIC_RE.finditer(src.text):
            self.graphics.append(Located(m.group(1).strip(), src.rel, src.line_of(m.start())))
        for m in NEWCMD_RE.finditer(src.text):
            name = m.group(1)
            self.commands.setdefault(name, []).append(
                Located(name, src.rel, src.line_of(m.start()))
            )
        for m in BIBRESOURCE_RE.finditer(src.text):
            for f in m.group(1).split(","):
                f = f.strip()
                if f:
                    self.bibfiles.append(f)
        self._scan_environments(src)
        self._scan_floats(src)
        self._scan_prose(src)

    def _scan_environments(self, src: Source) -> None:
        """Capture math and theorem bodies — the candidate spans for R1/R4/R5."""
        for env in sorted(MATH_ENVS | THEORY_ENVS):
            pattern = re.compile(
                r"\\begin\s*\{%s\*?\}(?P<body>.*?)\\end\s*\{%s\*?\}" % (env, env),
                re.DOTALL,
            )
            for m in pattern.finditer(src.text):
                body = m.group("body")
                labels = [x.group(1).strip() for x in LABEL_RE.finditer(body)]
                self.environments.append(
                    EnvBlock(
                        env=env,
                        label=labels[0] if labels else "",
                        body=normalize_ws(body)[:4000],
                        file=src.rel,
                        line=src.line_of(m.start()),
                        symbols=sorted(extract_symbols(body)) if env in MATH_ENVS else [],
                    )
                )

    def _scan_floats(self, src: Source) -> None:
        """Map each float's \\label to the table body it \\inputs."""
        depth = 0
        cur_labels: List[str] = []
        cur_inputs: List[str] = []
        cur_kind = ""
        cur_raw: List[str] = []
        for raw in src.lines:
            for m in BEGIN_RE.finditer(raw):
                env = m.group(1).strip()
                if env in FLOAT_ENVS:
                    if depth == 0:
                        cur_labels, cur_inputs, cur_raw = [], [], []
                        cur_kind = "figure" if env.startswith("figure") else "table"
                    depth += 1
            if depth > 0:
                cur_raw.append(raw)
                for m in LABEL_RE.finditer(raw):
                    cur_labels.append(m.group(1).strip())
                for m in INPUT_RE.finditer(raw):
                    cur_inputs.append(m.group(1).strip())
                for m in GRAPHIC_RE.finditer(raw):
                    cur_inputs.append(m.group(1).strip())
            for m in END_RE.finditer(raw):
                if m.group(1).strip() in FLOAT_ENVS:
                    depth = max(0, depth - 1)
                    if depth == 0:
                        blob = "\n".join(cur_raw)
                        cap = re.search(r"\\caption\s*\{(.+?)\}\s*(?:\\label|$)", blob, re.DOTALL)
                        notes = re.findall(r"\\item\s*(.+?)(?=\\item|\\end\s*\{tablenotes\}|$)", blob, re.DOTALL)
                        if not notes:
                            notes = re.findall(r"\\textit\s*\{Notes?:?\}(.+?)(?=\\end|$)", blob, re.DOTALL)
                        for lab in cur_labels:
                            self.float_context[lab] = {
                                "caption": normalize_ws(clean_cell(cap.group(1))) if cap else "",
                                "notes": [normalize_ws(clean_cell(n))[:1500] for n in notes if n.strip()],
                            }
                            self.label_kind[lab] = cur_kind
                            for tgt in cur_inputs:
                                resolved = self._resolve_input(tgt, src.path)
                                if resolved is not None and resolved.suffix == ".tex":
                                    rel = os.path.relpath(resolved, self.root)
                                    self.label_to_table[lab] = rel
                                    self.tables.setdefault(rel, TableDoc(rel))
                        cur_labels, cur_inputs, cur_raw = [], [], []

    def _scan_prose(self, src: Source) -> None:
        """Collect prose paragraphs, skipping preamble and float bodies."""
        in_doc = "\\begin{document}" not in src.text  # section files have no preamble
        depth = 0
        in_abstract = False
        buf: List[str] = []
        start = 0
        section = ""

        def flush() -> None:
            nonlocal buf, start
            if buf:
                text = normalize_ws(" ".join(buf))
                if text:
                    self.paragraphs.append(
                        Paragraph(
                            text=text,
                            file=src.rel,
                            line=start,
                            zone="abstract" if in_abstract else "body",
                            section=section,
                        )
                    )
            buf = []

        for i, raw in enumerate(src.lines, start=1):
            if not in_doc:
                if "\\begin{document}" in raw:
                    in_doc = True
                continue
            if "\\begin{abstract}" in raw:
                flush()
                in_abstract = True
                continue
            if "\\end{abstract}" in raw:
                flush()
                in_abstract = False
                continue
            opens = [m.group(1).strip() for m in BEGIN_RE.finditer(raw)]
            closes = [m.group(1).strip() for m in END_RE.finditer(raw)]
            entering = any(e in FLOAT_ENVS for e in opens)
            leaving = any(e in FLOAT_ENVS for e in closes)
            if entering:
                flush()
                depth += len([e for e in opens if e in FLOAT_ENVS])
            if leaving:
                depth = max(0, depth - len([e for e in closes if e in FLOAT_ENVS]))
                buf = []
                continue
            if depth > 0:
                continue
            m_sec = SECTION_RE.search(raw)
            if m_sec:
                flush()
                section = "%s:%d" % (src.rel, i)
            if not raw.strip():
                flush()
                start = 0
                continue
            if not buf:
                start = i
            buf.append(raw)
        flush()

        for para in self.paragraphs:
            if para.file != src.rel:
                continue
            para.refs = extract_refs(para.text)
            para.numbers = extract_prose_numbers(para.text, para.file, para.line)

    # -- bibliography ------------------------------------------------------

    def _load_bib(self) -> None:
        seen: Set[Path] = set()
        search: List[Path] = []
        for f in self.bibfiles:
            for base in (self.main.parent, self.root):
                for suffix in ("", ".bib"):
                    search.append(base / (f + suffix))
        # Fall back to any .bib beside the main file or at the project root.
        search.extend(self.main.parent.glob("*.bib"))
        search.extend(self.root.glob("*.bib"))
        for cand in search:
            if not cand.is_file() or cand.resolve() in seen:
                continue
            seen.add(cand.resolve())
            try:
                text = cand.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in BIBKEY_RE.finditer(text):
                self.bibkeys.add(m.group(1).strip())

    # -- table bodies ------------------------------------------------------

    def _load_tables(self) -> None:
        tables_dir = self.main.parent / "tables"
        if tables_dir.is_dir():
            for p in sorted(tables_dir.glob("*.tex")):
                self.tables.setdefault(os.path.relpath(p, self.root), TableDoc(os.path.relpath(p, self.root)))
        for rel, doc in self.tables.items():
            path = self.root / rel
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            text = "\n".join(strip_comments(ln) for ln in text.splitlines())
            doc.wrapped = bool(
                re.search(r"\\begin\s*\{table\*?\}", text) or re.search(r"\\caption\s*\{", text)
            )
            parse_tabular_into(text, doc)


# --------------------------------------------------------------------------
# Number extraction
# --------------------------------------------------------------------------

# A "claim number" carries a decimal point or thousands separators. Bare small
# integers (indices, counts of robustness checks, `\ell = -3`) are excluded on
# purpose: matching them against tables produces noise, not findings.
NUMBER_RE = re.compile(
    r"(?<![\w.])"
    r"(?P<sign>[-−]|\\text\{-\}|\$-\$)?\s*"
    r"(?P<num>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+)"
    r"(?![\w])"
)

SE_LEAD = re.compile(
    r"(standard error|std\.? ?err|s\.e\.|SE)\s*(of|is|=|:)?\s*$", re.IGNORECASE
)
P_LEAD = re.compile(r"(p[\s\-]?(value)?\s*[=<>]\s*|\$p\s*[=<>]\s*)$", re.IGNORECASE)
STAT_LEAD = re.compile(r"\b([FtzR]\^?2?|chi\^?2|F-stat[a-z]*)\s*[=]\s*$")
DERIVED_TRAIL = re.compile(
    r"^\s*~?\s*(percent|per ?cent|%|percentage points?)?\s*"
    r"(increase|decrease|change|rise|fall|larger|smaller)?\s*"
    r"(relative to|of the|compared (?:to|with))\s*(the\s*)?(baseline|mean|control)",
    re.IGNORECASE,
)
PP_TRAIL = re.compile(r"^\s*~?\s*(percentage[ ~]points?|p\.?p\.?)\b", re.IGNORECASE)
PCT_TRAIL = re.compile(r"^\s*~?\s*(percent|per ?cent|%)\b", re.IGNORECASE)
YEAR_RANGE_RE = re.compile(r"\b(1[89]\d{2}|20\d{2})\s*(--|–|-|to)\s*(1[89]\d{2}|20\d{2})\b")

# "per 100,000" is a rate denominator, not a claim about a table cell.
DENOM_LEAD = re.compile(r"\bper[\s~]*$", re.IGNORECASE)
# A cutoff in a sample definition ("families with INR $\le 1.49$", "share above
# 0.5") is a design parameter, not a result. It will not be in a results table.
THRESHOLD_LEAD = re.compile(
    r"(\\l(?:e|eq|eqslant)|\\g(?:e|eq|eqslant)|\\neq|[<>=]|\\pm|"
    r"\b(?:above|below|at least|at most|exceed(?:s|ing)?|greater than|less than|"
    r"more than|fewer than|threshold of|cutoff of|up to)\b)[\s~$]*$",
    re.IGNORECASE,
)
# Hedged figures are usually derived or rounded by hand; a mismatch is weak evidence.
HEDGE_LEAD = re.compile(
    r"\b(roughly|approximately|approx\.?|about|around|nearly|almost|some|circa|~)[\s~]*$",
    re.IGNORECASE,
)
# Numbers the author says are not in a table cannot be checked against one.
UNREPORTED_RE = re.compile(
    r"\b(not shown|not reported|unreported|not tabulated|available (?:up)?on request|"
    r"results omitted|omitted for brevity)\b",
    re.IGNORECASE,
)
# Confidence-interval bounds usually live in text or figures, not table cells.
INTERVAL_LEAD = re.compile(r"(CI|confidence interval|interval)[^\[\(]{0,20}[\[\(][^\[\(]{0,20}$", re.IGNORECASE)


def _clean_sign(sign: Optional[str]) -> float:
    if not sign:
        return 1.0
    return -1.0 if sign.strip() in {"-", "−", "\\text{-}", "$-$"} else 1.0


def decimals(raw: str) -> int:
    if "." not in raw:
        return 0
    return len(raw.split(".", 1)[1])


def extract_refs(text: str) -> List[str]:
    out: List[str] = []
    for m in REF_RE.finditer(text):
        for key in m.group(1).split(","):
            key = key.strip()
            if key:
                out.append(key)
    return out


def _mask_noise(text: str) -> str:
    """Blank out spans whose numbers are never empirical claims."""
    masked = text
    for pattern in (CITE_RE, LABEL_RE, REF_RE, INPUT_RE, GRAPHIC_RE):
        masked = pattern.sub(lambda m: " " * len(m.group(0)), masked)
    # Year ranges: 2005--2012
    masked = YEAR_RANGE_RE.sub(lambda m: " " * len(m.group(0)), masked)
    return masked


def extract_prose_numbers(text: str, file: str, line: int) -> List[ProseNumber]:
    # LaTeX writes thousands as 54{,}145 to control spacing; normalize so the
    # count is seen as one number rather than "54" and "145".
    text = re.sub(r"(?<=\d)\{,\}(?=\d)", ",", text)
    masked = _mask_noise(text)
    out: List[ProseNumber] = []
    for m in NUMBER_RE.finditer(masked):
        raw = m.group("num")
        after = masked[m.end() : m.end() + 60]
        if UNIT_RE.match(after):
            continue
        before = masked[max(0, m.start() - 40) : m.start()]
        try:
            value = float(raw.replace(",", "")) * _clean_sign(m.group("sign"))
        except ValueError:
            continue

        # Rate denominators ("per 100,000") are units, not claims. Drop them
        # outright — they were the single largest source of noise in testing.
        if DENOM_LEAD.search(before) or THRESHOLD_LEAD.search(before):
            continue

        kind = "estimate"
        if P_LEAD.search(before):
            kind = "pvalue"
        elif SE_LEAD.search(before):
            kind = "se"
        elif STAT_LEAD.search(before):
            kind = "stat"
        elif INTERVAL_LEAD.search(before):
            kind = "interval"
        elif DERIVED_TRAIL.match(after):
            kind = "derived"
        elif HEDGE_LEAD.search(before):
            kind = "approx"
        elif "," in raw and "." not in raw:
            kind = "count"

        # An explicitly unreported figure has no table cell to match by
        # construction; the author already told us so.
        window = masked[max(0, m.start() - 140) : m.end() + 140]
        if UNREPORTED_RE.search(window):
            kind = "unreported"

        if kind == "estimate" and PCT_TRAIL.match(after) and not PP_TRAIL.match(after):
            # A bare "27 percent" that is not a percentage-point effect is
            # usually a share or a derived ratio; treat as derived unless it
            # also reads as a level.
            if DERIVED_TRAIL.search(masked[m.end() : m.end() + 90]):
                kind = "derived"

        ctx_start = max(0, m.start() - 70)
        context = normalize_ws(text[ctx_start : m.end() + 70]) if len(text) >= m.end() else raw
        out.append(
            ProseNumber(
                raw=raw,
                value=value,
                kind=kind,
                file=file,
                line=line,
                context=context,
            )
        )
    return out


# --------------------------------------------------------------------------
# Tabular parsing
# --------------------------------------------------------------------------

TABULAR_BODY_RE = re.compile(
    r"\\begin\s*\{(tabular\*?|tabularx|tblr|longtable|talltblr)\}"
    r"(?:\s*\[[^\]]*\])?(?:\s*\{[^}]*\})*(?P<body>.*?)"
    r"\\end\s*\{\1\}",
    re.DOTALL,
)
RULE_RE = re.compile(r"\\(top|mid|bottom|cmid)rule(?:\([^)]*\))?(?:\{[^}]*\})?|\\hline")
MULTICOL_RE = re.compile(r"\\multicolumn\s*\{\d+\}\s*\{[^}]*\}\s*\{(.*?)\}", re.DOTALL)
TEXT_WRAP_RE = re.compile(r"\\(?:textit|textbf|emph|texttt|textsc|mathrm|text)\s*\{([^{}]*)\}")
SE_CELL_RE = re.compile(r"^\(\s*(?P<body>[^()]*)\s*\)$")
STAR_RE = re.compile(r"(\*+|\\\*|\$\^\{?\*+\}?\$)")


def clean_cell(cell: str) -> str:
    s = cell
    s = MULTICOL_RE.sub(lambda m: m.group(1), s)
    for _ in range(3):
        s = TEXT_WRAP_RE.sub(lambda m: m.group(1), s)
    s = s.replace("\\,", "").replace("\\ ", " ").replace("\\%", "%")
    s = re.sub(r"\\(?:num|si|SI)\s*\{([^}]*)\}", lambda m: m.group(1), s)
    s = re.sub(r"\\[a-zA-Z@]+\s*", " ", s)
    s = s.replace("{", " ").replace("}", " ").replace("$", "")
    return normalize_ws(s)


def parse_tabular_into(text: str, doc: TableDoc) -> None:
    bodies = [m.group("body") for m in TABULAR_BODY_RE.finditer(text)]
    if not bodies:
        bodies = [text]
    panel = ""
    for body in bodies:
        for raw_row in re.split(r"\\\\", body):
            row = RULE_RE.sub(" ", raw_row)
            row = re.sub(r"^\s*\[[^\]]*\]", " ", row)  # strip \\[0.5em] spacing arg
            if not row.strip():
                continue
            cells = [clean_cell(c) for c in row.split("&")]
            if not any(cells):
                continue
            doc.rows.append(cells)
            label = cells[0] if cells else ""
            if re.search(r"\bpanel\b", label, re.IGNORECASE) or (
                len(cells) == 1 and re.search(r"\bpanel\b", cells[0], re.IGNORECASE)
            ):
                panel = label
                continue
            for col, cell in enumerate(cells):
                if col == 0:
                    continue
                doc.numbers.extend(_cell_numbers(cell, label, col, panel))


def _cell_numbers(cell: str, row_label: str, col: int, panel: str) -> List[TableNumber]:
    if not cell:
        return []
    stars = 0
    m_star = STAR_RE.search(cell)
    if m_star:
        stars = m_star.group(0).count("*")
    stripped = STAR_RE.sub("", cell).strip()
    kind = "point"
    m_se = SE_CELL_RE.match(stripped)
    if m_se:
        kind = "se"
        stripped = m_se.group("body")
    out: List[TableNumber] = []
    for m in NUMBER_RE.finditer(stripped):
        raw = m.group("num")
        after = stripped[m.end() : m.end() + 20]
        if UNIT_RE.match(after):
            continue
        try:
            value = float(raw.replace(",", "")) * _clean_sign(m.group("sign"))
        except ValueError:
            continue
        k = kind
        if k == "point" and "," in raw and "." not in raw:
            k = "count"
        out.append(
            TableNumber(
                raw=raw,
                value=value,
                kind=k,
                row_label=row_label,
                col=col,
                panel=panel,
                stars=stars,
            )
        )
    return out


# --------------------------------------------------------------------------
# Matching
# --------------------------------------------------------------------------


def matches(prose: ProseNumber, table_value: float) -> bool:
    """Rounding-tolerant match, allowing a percentage-point rescale and sign loss.

    Prose reports "4.9 percentage points" for a table cell of 0.0489; "$-0.017$"
    for -0.0170; "standard error 0.016" for (0.0162). All three are the same
    number stated at different precision and scale.
    """
    nd = decimals(prose.raw)
    for candidate in (table_value, table_value * 100.0):
        for signed in (candidate, -candidate):
            if abs(round(signed, nd) - prose.value) < 10 ** (-(nd + 6)):
                return True
    return False


def any_match(prose: ProseNumber, numbers: Sequence[TableNumber]) -> Optional[TableNumber]:
    # Prefer a same-kind match (prose SE against a table SE cell) so the
    # evidence line names the right cell, but accept any cell.
    ordered = sorted(numbers, key=lambda t: 0 if t.kind == prose.kind else 1)
    for tn in ordered:
        if matches(prose, tn.value):
            return tn
    return None


def edit_distance(a: str, b: str, cap: int = 3) -> int:
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
        if min(prev) > cap:
            return cap + 1
    return prev[-1]


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------


def check_references(idx: Index) -> List[Finding]:
    out: List[Finding] = []
    defined = set(idx.labels)
    for ref in idx.refs:
        if ref.value in defined:
            continue
        near = [d for d in defined if edit_distance(ref.value, d, 2) <= 2]
        suggestion = ""
        autofix = False
        if len(near) == 1:
            suggestion = "Change to \\cref{%s}." % near[0]
            autofix = True
        elif near:
            suggestion = "Closest defined labels: " + ", ".join(sorted(near)[:4])
        out.append(
            Finding(
                check="undefined-ref",
                severity="major",
                file=ref.file,
                line=ref.line,
                message="Reference to `%s` has no matching \\label." % ref.value,
                evidence="\\ref{%s}" % ref.value,
                suggestion=suggestion,
                autofix=autofix,
            )
        )
    referenced = {r.value for r in idx.refs}
    for label, locs in sorted(idx.labels.items()):
        if len(locs) > 1:
            out.append(
                Finding(
                    check="duplicate-label",
                    severity="major",
                    file=locs[1].file,
                    line=locs[1].line,
                    message="Label `%s` is defined %d times." % (label, len(locs)),
                    evidence="also at " + ", ".join("%s:%d" % (l.file, l.line) for l in locs[:-1]),
                    suggestion="Give each float, equation, or section a unique label.",
                )
            )
        if label in referenced:
            continue
        # Only pointable objects count. An unreferenced \label{sec:...} is
        # normal practice; an unreferenced table is a table the reader never
        # gets told to look at.
        kind = idx.label_kind.get(label, "")
        if not kind:
            if re.match(r"^(tab|table)[:.]", label):
                kind = "table"
            elif re.match(r"^(fig|figure)[:.]", label):
                kind = "figure"
            elif re.match(r"^(eq|eqn|equation)[:.]", label):
                kind = "equation"
        if kind not in {"table", "figure", "equation"}:
            continue
        out.append(
            Finding(
                check="orphan-float",
                severity="minor",
                file=locs[0].file,
                line=locs[0].line,
                message="%s `%s` is never referenced in the text." % (kind.capitalize(), label),
                suggestion=(
                    "Every table and figure should be discussed and cross-referenced with "
                    "\\cref{}, or removed."
                ),
            )
        )
    return out


def check_citations(idx: Index) -> List[Finding]:
    out: List[Finding] = []
    if not idx.bibkeys:
        return out
    for cite in idx.cites:
        if cite.value in idx.bibkeys:
            continue
        near = [k for k in idx.bibkeys if edit_distance(cite.value, k, 3) <= 3]
        out.append(
            Finding(
                check="undefined-cite",
                severity="major",
                file=cite.file,
                line=cite.line,
                message="Citation key `%s` is not in the bibliography." % cite.value,
                evidence="\\cite{%s}" % cite.value,
                suggestion=(
                    "Closest keys: " + ", ".join(sorted(near)[:4]) if near else "Add the entry to the .bib file."
                ),
            )
        )
    return out


def check_files(idx: Index) -> List[Finding]:
    out: List[Finding] = []
    for loc in idx.missing_inputs:
        out.append(
            Finding(
                check="missing-input",
                severity="major",
                file=loc.file,
                line=loc.line,
                message="\\input{%s} does not resolve to a file." % loc.value,
                suggestion="Create the file or fix the path.",
            )
        )
    figdirs = [idx.main.parent, idx.main.parent / "figures", idx.root]
    for loc in idx.graphics:
        target = loc.value
        found = False
        cands: List[Path] = []
        for base in figdirs:
            cands.append(base / target)
            for ext in (".pdf", ".png", ".jpg", ".jpeg", ".eps"):
                cands.append(base / (target + ext))
        for c in cands:
            if c.is_file():
                found = True
                break
        if found:
            continue
        stem = Path(target).stem
        alts = []
        figdir = idx.main.parent / "figures"
        if figdir.is_dir():
            alts = [p.name for p in figdir.iterdir() if p.stem == stem]
        out.append(
            Finding(
                check="missing-graphic",
                severity="major",
                file=loc.file,
                line=loc.line,
                message="\\includegraphics{%s} does not resolve to a file." % target,
                suggestion=(
                    "Found `figures/%s` — fix the extension." % alts[0]
                    if len(alts) == 1
                    else "Generate the figure or fix the path."
                ),
                autofix=len(alts) == 1,
            )
        )
    return out


def check_structure(idx: Index) -> List[Finding]:
    """INV-13 and INV-23: table bodies stay bare, floats stay out of sections."""
    out: List[Finding] = []
    for rel, doc in sorted(idx.tables.items()):
        if doc.wrapped:
            out.append(
                Finding(
                    check="table-file-wrapped",
                    severity="minor",
                    file=rel,
                    line=1,
                    message="Table body contains \\begin{table} or \\caption (INV-13).",
                    suggestion="Export a bare tabular; wrap it in main.tex.",
                )
            )
    for rel, src in sorted(idx.sources.items()):
        if "sections/" not in rel.replace(os.sep, "/"):
            continue
        for i, line in enumerate(src.lines, start=1):
            m = BEGIN_RE.search(line)
            if m and m.group(1).strip() in FLOAT_ENVS:
                out.append(
                    Finding(
                        check="float-in-section",
                        severity="minor",
                        file=rel,
                        line=i,
                        message="Float `%s` declared inside a section file (INV-23)." % m.group(1),
                        suggestion="Move it to the TABLES/FIGURES block at the end of main.tex.",
                    )
                )
    for name, locs in sorted(idx.commands.items()):
        if len(locs) > 1 and not any("renewcommand" in idx.sources[l.file].lines[l.line - 1] for l in locs[1:] if l.file in idx.sources and l.line - 1 < len(idx.sources[l.file].lines)):
            out.append(
                Finding(
                    check="duplicate-macro",
                    severity="minor",
                    file=locs[1].file,
                    line=locs[1].line,
                    message="Macro \\%s is defined more than once." % name,
                    evidence="also at " + ", ".join("%s:%d" % (l.file, l.line) for l in locs[:-1]),
                    suggestion="One definition per macro — a redefinition silently changes notation (INV-7).",
                )
            )
    return out


def check_numbers(idx: Index) -> List[Finding]:
    """Numbers in a paragraph that cites a table must appear in that table."""
    out: List[Finding] = []
    all_table_numbers: List[TableNumber] = []
    for doc in idx.tables.values():
        all_table_numbers.extend(doc.numbers)
    # With no parsed table cells there is nothing to check against. Staying
    # silent beats inventing findings about tables we could not read.
    if not all_table_numbers:
        return out

    # A paper cites a table once and then discusses it for several paragraphs.
    # Anchoring per-paragraph would leave most claims unchecked, so the table
    # context carries forward until the next section heading resets it.
    active: List[str] = []
    active_section = object()

    for para in idx.paragraphs:
        if para.section != active_section:
            active_section = para.section
            active = []
        explicit = [
            idx.label_to_table[r]
            for r in para.refs
            if r in idx.label_to_table and idx.label_to_table[r] in idx.tables
        ]
        if explicit:
            active = explicit
            inherited = False
        else:
            inherited = bool(active)
        cited = explicit or active
        pool: List[TableNumber] = []
        for rel in cited:
            pool.extend(idx.tables[rel].numbers)
        anchor = ", ".join(sorted(set(cited)))
        via = " (carried from the cross-reference earlier in this section)" if inherited else ""

        for num in para.numbers:
            if num.kind in {"pvalue", "stat", "derived", "interval", "unreported"}:
                continue
            # A hedged figure ("roughly 5.7") is usually a hand-derived number.
            # Worth surfacing, not worth blocking a commit over.
            sev = "minor" if num.kind == "approx" else "major"
            # Distinguish a *stale* number from an *untabulated* one. "Mean age
            # 30.8" against a cell of 35.5 is a value that went stale. "49.8
            # percent of weights are negative" against a nearest cell three
            # orders of magnitude away was never in a table at all — that is a
            # traceability gap (INV-22), not a contradiction, and it must not
            # block. The nearest-cell distance separates the two cases.
            if sev == "major" and not _plausibly_tabulated(num, pool or all_table_numbers):
                sev = "minor"
            if pool:
                hit = any_match(num, pool)
                if hit is not None:
                    continue
                # Not in the cited table — is it anywhere else? That is a
                # weaker finding (wrong table cited, or number from the text).
                elsewhere = any_match(num, all_table_numbers)
                if elsewhere is not None:
                    out.append(
                        Finding(
                            check="number-wrong-table",
                            severity="minor",
                            file=num.file,
                            line=num.line,
                            message=(
                                "%s is not in %s%s but appears in another table."
                                % (num.raw, anchor, via)
                            ),
                            evidence=num.context,
                            suggestion="Check whether the cross-reference points at the right table.",
                        )
                    )
                else:
                    out.append(
                        Finding(
                            check="number-mismatch",
                            severity=sev,
                            file=num.file,
                            line=num.line,
                            message=(
                                "%s appears in prose discussing %s%s, and no cell in any table "
                                "rounds to it." % (num.raw, anchor, via)
                            ),
                            evidence=num.context,
                            suggestion=_nearest_cell_hint(num, pool),
                        )
                    )
            elif para.zone == "abstract":
                # Abstract numbers carry no cross-reference, so search everything.
                if any_match(num, all_table_numbers) is None:
                    out.append(
                        Finding(
                            check="abstract-number-unsourced",
                            severity=sev,
                            file=num.file,
                            line=num.line,
                            message="%s in the abstract does not appear in any table." % num.raw,
                            evidence=num.context,
                            suggestion=_nearest_cell_hint(num, all_table_numbers),
                        )
                    )
    return out


def _plausibly_tabulated(num: ProseNumber, pool: Sequence[TableNumber]) -> bool:
    """Is there a cell close enough that this number was plausibly meant to be it?

    A stale value sits near its correct cell — prose 30.8 against a cell of 35.5.
    A number that was never tabulated sits nowhere near anything. Compare on
    relative distance so the test works for both 0.0489 and 108,766.
    """
    target = abs(num.value)
    if target == 0:
        return True
    best = None
    for tn in pool:
        for scale in (1.0, 100.0, 0.01):
            cand = abs(tn.value * scale)
            if cand == 0:
                continue
            rel = abs(cand - target) / max(target, cand)
            best = rel if best is None else min(best, rel)
    # Within 40% of some cell: close enough that the author meant that cell and
    # one of the two is stale. Beyond that, the number lives only in the text.
    return best is not None and best <= 0.40


def _nearest_cell_hint(num: ProseNumber, pool: Sequence[TableNumber]) -> str:
    if not pool:
        return "No table cells available to compare against."
    best = None
    best_gap = None
    for tn in pool:
        for scale in (1.0, 100.0):
            gap = abs(abs(tn.value * scale) - abs(num.value))
            if best_gap is None or gap < best_gap:
                best_gap, best = gap, tn
    if best is None:
        return ""
    where = best.row_label or "row"
    if best.panel:
        where = "%s / %s" % (best.panel, where)
    return "Nearest cell: %s (%s, column %d). Reconcile the prose with the table." % (
        best.raw,
        where,
        best.col,
    )


def check_derived_arithmetic(idx: Index) -> List[Finding]:
    """Check 'X percent increase relative to a baseline of Y' against X/Y."""
    out: List[Finding] = []
    pattern = re.compile(
        r"(?P<pct>\d+(?:\.\d+)?)\s*~?\s*(?:percent|per ?cent|%)\s*"
        r"(?:increase|decrease|change|rise|fall)?\s*"
        r"relative to (?:the\s*)?(?:a\s*)?(?P<what>[^.]{0,60}?)"
        r"(?P<base>\d+(?:\.\d+)?)\s*~?\s*(?:percent|per ?cent|%)",
        re.IGNORECASE,
    )
    for para in idx.paragraphs:
        for m in pattern.finditer(para.text):
            try:
                pct = float(m.group("pct"))
                base = float(m.group("base"))
            except ValueError:
                continue
            if base == 0:
                continue
            effects = [
                n.value
                for n in para.numbers
                if n.kind == "estimate" and abs(n.value) > 0 and abs(n.value) != base
            ]
            if not effects:
                continue
            implied = [abs(e) / base * 100.0 for e in effects]
            # An effect stated in percentage points against a baseline in
            # percent: the ratio is effect/baseline.
            if any(abs(r - pct) <= max(1.0, 0.05 * pct) for r in implied):
                continue
            out.append(
                Finding(
                    check="derived-arithmetic",
                    severity="minor",
                    file=para.file,
                    line=para.line,
                    message=(
                        "Stated %.4g%% relative change against a baseline of %.4g does not follow "
                        "from any effect size in this paragraph." % (pct, base)
                    ),
                    evidence=normalize_ws(m.group(0)),
                    suggestion=(
                        "Implied by the effects stated here: "
                        + ", ".join("%.1f%%" % r for r in sorted(implied)[:4])
                    ),
                )
            )
    return out


def check_significance(idx: Index) -> List[Finding]:
    """Stars in a cited table vs the p-value the prose reports for it."""
    out: List[Finding] = []
    for para in idx.paragraphs:
        cited = [idx.label_to_table[r] for r in para.refs if r in idx.label_to_table]
        pool: List[TableNumber] = []
        for rel in cited:
            if rel in idx.tables:
                pool.extend(idx.tables[rel].numbers)
        if not pool:
            continue
        nums = para.numbers
        for i, num in enumerate(nums):
            if num.kind != "pvalue":
                continue
            # The estimate this p-value belongs to is the nearest preceding
            # estimate in the same sentence.
            est = None
            for j in range(i - 1, -1, -1):
                if nums[j].kind == "estimate":
                    est = nums[j]
                    break
            if est is None:
                continue
            cell = any_match(est, [t for t in pool if t.kind == "point"])
            if cell is None:
                continue
            p = num.value
            stars = cell.stars
            expected = 3 if p < 0.01 else 2 if p < 0.05 else 1 if p < 0.10 else 0
            if stars == expected:
                continue
            out.append(
                Finding(
                    check="significance-mismatch",
                    severity="minor",
                    file=num.file,
                    line=num.line,
                    message=(
                        "Prose reports p = %s for %s, but the table cell carries %d star(s) "
                        "(p < %s implies %d)." % (num.raw, est.raw, stars, num.raw, expected)
                    ),
                    evidence=num.context,
                    suggestion="Reconcile the star thresholds in the table note with the reported p-value.",
                )
            )
    return out


def run_checks(idx: Index) -> List[Finding]:
    findings: List[Finding] = []
    findings += check_references(idx)
    findings += check_citations(idx)
    findings += check_files(idx)
    findings += check_structure(idx)
    findings += check_numbers(idx)
    findings += check_derived_arithmetic(idx)
    findings += check_significance(idx)
    return sorted(findings, key=lambda f: f.sort_key())


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

CHECK_TITLES = {
    "undefined-ref": "Undefined cross-reference",
    "duplicate-label": "Duplicate label",
    "orphan-float": "Table or figure never referenced in the text",
    "undefined-cite": "Citation key not in bibliography",
    "missing-input": "Missing \\input target",
    "missing-graphic": "Missing figure file",
    "table-file-wrapped": "Table body is not bare (INV-13)",
    "float-in-section": "Float inside a section file (INV-23)",
    "duplicate-macro": "Macro defined twice (INV-7)",
    "number-mismatch": "Number does not match the cited table (INV-11)",
    "number-wrong-table": "Number is in a different table than the one cited",
    "abstract-number-unsourced": "Abstract number not found in any table (INV-11)",
    "derived-arithmetic": "Derived percentage does not follow",
    "significance-mismatch": "Stars and reported p-value disagree",
}


def render_markdown(idx: Index, findings: List[Finding], date: str) -> str:
    major = [f for f in findings if f.severity == "major"]
    minor = [f for f in findings if f.severity == "minor"]
    info = [f for f in findings if f.severity == "info"]

    lines: List[str] = []
    lines.append("# Coherence Audit")
    lines.append("")
    lines.append("**Date:** %s  " % date)
    lines.append("**Paper:** `%s`  " % os.path.relpath(idx.main, idx.root))
    lines.append("**Engine:** deterministic layer v%s" % VERSION)
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    if major:
        lines.append("**FAIL** — %d blocking finding%s." % (len(major), "" if len(major) == 1 else "s"))
    else:
        lines.append("**PASS** — no blocking findings.")
    lines.append("")
    lines.append("| Severity | Count | Blocking |")
    lines.append("|---|---:|---|")
    lines.append("| Major | %d | yes |" % len(major))
    lines.append("| Minor | %d | no |" % len(minor))
    lines.append("| Info | %d | no |" % len(info))
    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    lines.append("| Structure | Count |")
    lines.append("|---|---:|")
    lines.append("| Source files parsed | %d |" % len(idx.sources))
    lines.append("| Labels defined | %d |" % len(idx.labels))
    lines.append("| References resolved | %d |" % len(idx.refs))
    lines.append("| Citation keys used | %d |" % len({c.value for c in idx.cites}))
    lines.append("| Bibliography entries | %d |" % len(idx.bibkeys))
    lines.append("| Table bodies parsed | %d |" % len(idx.tables))
    lines.append(
        "| Numeric cells indexed | %d |" % sum(len(d.numbers) for d in idx.tables.values())
    )
    lines.append("| Prose paragraphs | %d |" % len(idx.paragraphs))
    lines.append(
        "| Claim numbers checked | %d |"
        % sum(
            1
            for p in idx.paragraphs
            for n in p.numbers
            if n.kind in {"estimate", "se", "count"}
        )
    )
    lines.append("")

    if not findings:
        lines.append("## Findings")
        lines.append("")
        lines.append("None. Every cross-reference resolves, every citation key is in the")
        lines.append("bibliography, and every claim number in a paragraph citing a table")
        lines.append("appears in that table.")
        lines.append("")
        return "\n".join(lines)

    for title, group in (("Blocking", major), ("Non-blocking", minor), ("Informational", info)):
        if not group:
            continue
        lines.append("## %s" % title)
        lines.append("")
        for f in group:
            lines.append("### `%s` — %s:%d" % (f.check, f.file, f.line))
            lines.append("")
            lines.append("%s" % f.message)
            lines.append("")
            if f.evidence:
                lines.append("> %s" % f.evidence)
                lines.append("")
            if f.suggestion:
                lines.append("**Fix:** %s" % f.suggestion)
                lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "Deterministic layer only. Run `/coherence --deep` for the reasoning layer "
        "(estimand drift, claim strength vs evidence, cross-section contradictions)."
    )
    lines.append("")
    return "\n".join(lines)


def index_payload(idx: Index) -> dict:
    """The JSON the reasoning layer consumes. Keeps spans, drops raw source."""
    return {
        "version": VERSION,
        "root": str(idx.root),
        "main": os.path.relpath(idx.main, idx.root),
        "sources": sorted(idx.sources),
        "labels": {k: [{"file": l.file, "line": l.line} for l in v] for k, v in idx.labels.items()},
        "label_kind": idx.label_kind,
        "label_to_table": idx.label_to_table,
        "bib_entries": len(idx.bibkeys),
        "tables": {
            rel: {
                "rows": doc.rows,
                "numbers": [
                    {
                        "raw": n.raw,
                        "value": n.value,
                        "kind": n.kind,
                        "row": n.row_label,
                        "col": n.col,
                        "panel": n.panel,
                        "stars": n.stars,
                    }
                    for n in doc.numbers
                ],
            }
            for rel, doc in sorted(idx.tables.items())
        },
        "environments": [
            {
                "env": e.env,
                "label": e.label,
                "file": e.file,
                "line": e.line,
                "symbols": e.symbols,
                "body": e.body,
            }
            for e in idx.environments
        ],
        "paragraphs": [
            {
                "file": p.file,
                "line": p.line,
                "zone": p.zone,
                "refs": p.refs,
                "text": p.text,
                "numbers": [
                    {"raw": n.raw, "value": n.value, "kind": n.kind, "context": n.context}
                    for n in p.numbers
                ],
            }
            for p in idx.paragraphs
        ],
    }


# --------------------------------------------------------------------------
# Candidate slicing for the reasoning layer
# --------------------------------------------------------------------------

STRENGTH_WORDS = re.compile(
    r"\b(large|largely|substantial(?:ly)?|sizeable|sizable|considerable|strong(?:ly)?|"
    r"dramatic(?:ally)?|striking(?:ly)?|marked(?:ly)?|negligible|precise(?:ly)?|"
    r"robust(?:ly)?|economically (?:meaningful|significant)|modest|small)\b",
    re.IGNORECASE,
)
DIRECTION_WORDS = re.compile(
    r"\b(increase[sd]?|decrease[sd]?|raise[sd]?|reduce[sd]?|lower[sed]*|rise[sn]?|"
    r"fall[sen]*|improve[sd]?|worsen[sed]*|boost[sed]*|depress[esd]*)\b",
    re.IGNORECASE,
)
RESTRICTION_WORDS = re.compile(
    r"\b(sample (?:consists|includes|is restricted|covers)|we restrict|we (?:drop|exclude|keep)|"
    r"treatment is defined|defined as|we define|our sample|the period|covering|"
    r"we assume|assumption|conditional on|we cluster)\b",
    re.IGNORECASE,
)


def extract_symbols(body: str) -> Set[str]:
    out: Set[str] = set()
    for m in SYMBOL_RE.finditer(body):
        name = m.group(1) or m.group(2)
        if not name or name in SYMBOL_STOPWORDS:
            continue
        out.add(name)
    return out


def build_slices(idx: Index) -> Dict[str, dict]:
    """Per-check candidate sets. Each reasoning agent reads exactly one of these.

    The fan-out is only affordable because no agent sees the whole paper — a
    specification auditor gets equation bodies and the paragraphs citing them,
    nothing else.
    """
    eq_labels = {e.label for e in idx.environments if e.env in MATH_ENVS and e.label}

    # R1 — specification: equations plus the prose that cites them.
    spec_pairs = []
    for para in idx.paragraphs:
        hits = [r for r in para.refs if r in eq_labels]
        if not hits:
            continue
        spec_pairs.append(
            {
                "paragraph": {"file": para.file, "line": para.line, "text": para.text},
                "equations": [
                    {"label": e.label, "file": e.file, "line": e.line, "body": e.body}
                    for e in idx.environments
                    if e.label in hits
                ],
            }
        )

    # R2 + R6 — claims: sentences carrying a strength word or a direction verb
    # alongside a number, with the table cells that number resolves to.
    claim_spans = []
    for para in idx.paragraphs:
        has_number = any(n.kind in {"estimate", "se", "approx"} for n in para.numbers)
        if not has_number:
            continue
        if not (STRENGTH_WORDS.search(para.text) or DIRECTION_WORDS.search(para.text)):
            continue
        cited = [idx.label_to_table[r] for r in para.refs if r in idx.label_to_table]
        cells = []
        for rel in cited:
            for n in idx.tables.get(rel, TableDoc(rel)).numbers:
                cells.append(
                    {
                        "table": rel,
                        "raw": n.raw,
                        "value": n.value,
                        "kind": n.kind,
                        "row": n.row_label,
                        "col": n.col,
                        "panel": n.panel,
                        "stars": n.stars,
                    }
                )
        claim_spans.append(
            {
                "paragraph": {"file": para.file, "line": para.line, "text": para.text},
                "numbers": [
                    {"raw": n.raw, "value": n.value, "kind": n.kind} for n in para.numbers
                ],
                "cited_cells": cells,
            }
        )

    # R3 — continuity: statements of scope early vs restatements later.
    setup, restatement = [], []
    for para in idx.paragraphs:
        rec = {"file": para.file, "line": para.line, "text": para.text, "zone": para.zone}
        low = para.file.lower()
        is_setup = any(k in low for k in ("data", "strategy", "empirical", "background", "method"))
        is_late = any(k in low for k in ("result", "robust", "conclusion", "discussion"))
        if RESTRICTION_WORDS.search(para.text) and (is_setup or para.zone == "abstract"):
            setup.append(rec)
        elif is_late or para.zone == "abstract":
            restatement.append(rec)

    # R4 — notation: symbols used in more than one file.
    by_symbol: Dict[str, List[dict]] = {}
    for e in idx.environments:
        for s in e.symbols:
            by_symbol.setdefault(s, []).append(
                {"env": e.env, "label": e.label, "file": e.file, "line": e.line, "body": e.body}
            )
    shared = {
        s: uses
        for s, uses in by_symbol.items()
        if len({u["file"] for u in uses}) > 1 or len(uses) > 2
    }

    # R5 — theory: theorem-like bodies plus the assumption blocks.
    theory = [
        {"env": e.env, "label": e.label, "file": e.file, "line": e.line, "body": e.body}
        for e in idx.environments
        if e.env in THEORY_ENVS
    ]

    return {
        "specification": {"check": "R1", "candidates": spec_pairs},
        "claims": {"check": "R2+R6", "candidates": claim_spans},
        "continuity": {"check": "R3", "setup": setup, "restatements": restatement},
        "notation": {"check": "R4", "symbols": shared},
        "theory": {"check": "R5", "candidates": theory},
    }


def build_segments(idx: Index, min_words: int = 300) -> List[dict]:
    """Cut the paper into readable units for deep-read commenters.

    A segment is a (sub)section: its prose, plus every exhibit it points at.
    Commenters read a segment in full rather than a filtered keyhole — that is
    the difference between a checker and a reader. Each segment carries the
    tables and equations it cites so a commenter can judge a claim against the
    evidence without loading the whole paper.
    """
    # Cost scales with segment count, so undersized sections are merged into
    # their predecessor. A 54-word subsection is not worth its own reader, and
    # in the first production run those stubs were pure overhead.
    segments: List[dict] = []
    by_section: Dict[str, List[Paragraph]] = {}
    order: List[str] = []
    for para in idx.paragraphs:
        key = para.section or ("%s:top" % para.file)
        if key not in by_section:
            by_section[key] = []
            order.append(key)
        by_section[key].append(para)

    for key in order:
        paras = by_section[key]
        refs: List[str] = []
        for p in paras:
            refs.extend(p.refs)
        refs = sorted(set(refs))

        tables = []
        for r in refs:
            rel = idx.label_to_table.get(r)
            if rel and rel in idx.tables:
                ctx = idx.float_context.get(r, {})
                tables.append(
                    {
                        "label": r,
                        "path": rel,
                        "caption": ctx.get("caption", ""),
                        "notes": ctx.get("notes", []),
                        "rows": idx.tables[rel].rows,
                    }
                )
        figures = [
            {"label": r, "caption": idx.float_context.get(r, {}).get("caption", "")}
            for r in refs
            if idx.label_kind.get(r) == "figure"
        ]
        equations = [
            {"label": e.label, "file": e.file, "line": e.line, "body": e.body}
            for e in idx.environments
            if e.env in MATH_ENVS and e.label and e.label in refs
        ]
        theory = [
            {"env": e.env, "label": e.label, "file": e.file, "line": e.line, "body": e.body}
            for e in idx.environments
            if e.env in THEORY_ENVS and e.file == paras[0].file
        ]
        heading = paras[0].file
        text = "\n\n".join(p.text for p in paras)
        segments.append(
            {
                "id": "seg%02d" % (len(segments) + 1),
                "section": key,
                "file": heading,
                "start_line": paras[0].line,
                "zone": paras[0].zone,
                "paragraph_count": len(paras),
                "word_count": len(text.split()),
                "text": text,
                "refs": refs,
                "tables": tables,
                "figures": figures,
                "equations": equations,
                "theory": theory,
            }
        )

    merged: List[dict] = []
    for seg in segments:
        if merged and seg["word_count"] < min_words and merged[-1]["file"] == seg["file"]:
            prev = merged[-1]
            prev["text"] += "\n\n" + seg["text"]
            prev["word_count"] += seg["word_count"]
            prev["paragraph_count"] += seg["paragraph_count"]
            prev["refs"] = sorted(set(prev["refs"] + seg["refs"]))
            for key in ("tables", "figures", "equations", "theory"):
                seen = {json.dumps(x, sort_keys=True) for x in prev[key]}
                prev[key] += [x for x in seg[key] if json.dumps(x, sort_keys=True) not in seen]
            continue
        merged.append(seg)
    for i, seg in enumerate(merged, start=1):
        seg["id"] = "seg%02d" % i
    return merged


def write_segments(idx: Index, outdir: Path, min_words: int = 300) -> List[dict]:
    outdir.mkdir(parents=True, exist_ok=True)
    segs = build_segments(idx, min_words=min_words)
    manifest = []
    for seg in segs:
        (outdir / ("%s.json" % seg["id"])).write_text(
            json.dumps(seg, indent=2), encoding="utf-8"
        )
        manifest.append(
            {
                "id": seg["id"],
                "file": seg["file"],
                "start_line": seg["start_line"],
                "words": seg["word_count"],
                "paragraphs": seg["paragraph_count"],
                "tables": [t["label"] for t in seg["tables"]],
                "equations": [e["label"] for e in seg["equations"]],
                "theory_blocks": len(seg["theory"]),
            }
        )
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def write_slices(idx: Index, outdir: Path) -> Dict[str, int]:
    outdir.mkdir(parents=True, exist_ok=True)
    slices = build_slices(idx)
    counts: Dict[str, int] = {}
    for name, payload in slices.items():
        path = outdir / ("%s.json" % name)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        if "candidates" in payload:
            counts[name] = len(payload["candidates"])
        elif "symbols" in payload:
            counts[name] = len(payload["symbols"])
        else:
            counts[name] = len(payload.get("setup", [])) + len(payload.get("restatements", []))
    return counts


# --------------------------------------------------------------------------
# Autofix
# --------------------------------------------------------------------------


def apply_fixes(idx: Index, findings: List[Finding]) -> List[str]:
    """Apply only unambiguous mechanical fixes. Never touches a claim number."""
    applied: List[str] = []
    by_file: Dict[str, List[Finding]] = {}
    for f in findings:
        if not f.autofix:
            continue
        by_file.setdefault(f.file, []).append(f)

    for rel, group in by_file.items():
        path = idx.root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        original = text
        for f in group:
            if f.check == "undefined-ref":
                m = re.search(r"\\cref\{(.+?)\}", f.suggestion)
                bad = re.search(r"\\ref\{(.+?)\}", f.evidence)
                if not m or not bad:
                    continue
                text = re.sub(
                    r"(\\(?:c|C|auto|page|eq|v|f)?ref\s*\*?\s*\{)%s(\})" % re.escape(bad.group(1)),
                    lambda mm: mm.group(1) + m.group(1) + mm.group(2),
                    text,
                )
                applied.append("%s: %s -> %s" % (rel, bad.group(1), m.group(1)))
            elif f.check == "missing-graphic":
                alt = re.search(r"`figures/([^`]+)`", f.suggestion)
                bad = re.search(r"\\includegraphics\{(.+?)\}", f.message)
                if not alt or not bad:
                    continue
                new = "figures/" + alt.group(1)
                text = text.replace("{%s}" % bad.group(1), "{%s}" % new)
                applied.append("%s: %s -> %s" % (rel, bad.group(1), new))
        if text != original:
            path.write_text(text, encoding="utf-8")
    return applied


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def find_main(paper_dir: Path) -> Optional[Path]:
    for name in ("main.tex", "paper.tex", "manuscript.tex"):
        cand = paper_dir / name
        if cand.is_file():
            return cand
    texs = [
        p
        for p in sorted(paper_dir.glob("*.tex"))
        if "\\begin{document}" in p.read_text(encoding="utf-8", errors="replace")
    ]
    return texs[0] if texs else None


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic coherence audit for LaTeX papers.")
    ap.add_argument("--paper", default="paper", help="Directory holding the manuscript (default: paper)")
    ap.add_argument("--main", default=None, help="Main .tex file (default: auto-detect)")
    ap.add_argument("--root", default=".", help="Project root for relative paths (default: .)")
    ap.add_argument("--json", dest="json_out", default=None, help="Write the index + findings as JSON")
    ap.add_argument("--markdown", dest="md_out", default=None, help="Write the markdown report")
    ap.add_argument("--scope", default=None, help="Limit findings to one source file")
    ap.add_argument(
        "--min-severity",
        default="info",
        choices=("major", "minor", "info"),
        help="Suppress findings below this severity",
    )
    ap.add_argument(
        "--slices",
        default=None,
        help="Write per-check candidate sets for the reasoning-layer fan-out",
    )
    ap.add_argument(
        "--segments",
        default=None,
        help="Write per-section segments for the deep-read fan-out",
    )
    ap.add_argument(
        "--min-segment-words",
        type=int,
        default=300,
        help="Merge sections below this length into the previous segment (default 300)",
    )
    ap.add_argument(
        "--skeptic",
        action="store_true",
        help="Include the adversarial twin reader in the cost estimate (off by default)",
    )
    ap.add_argument("--fix", action="store_true", help="Apply unambiguous mechanical fixes")
    ap.add_argument("--quiet", action="store_true", help="Suppress stdout report")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    paper_dir = (root / args.paper) if not os.path.isabs(args.paper) else Path(args.paper)
    if args.main:
        main_tex = Path(args.main)
        if not main_tex.is_absolute():
            main_tex = root / args.main
    else:
        if not paper_dir.is_dir():
            sys.stderr.write("error: paper directory not found: %s\n" % paper_dir)
            return 2
        found = find_main(paper_dir)
        if found is None:
            sys.stderr.write("error: no main .tex found in %s\n" % paper_dir)
            return 2
        main_tex = found
    if not main_tex.is_file():
        sys.stderr.write("error: main file not found: %s\n" % main_tex)
        return 2

    idx = Index(root=root, main=main_tex)
    idx.build()
    findings = run_checks(idx)

    if args.scope:
        scope = os.path.relpath((root / args.scope).resolve(), root)
        findings = [f for f in findings if f.file == scope]
    threshold = SEVERITY_ORDER[args.min_severity]
    findings = [f for f in findings if SEVERITY_ORDER.get(f.severity, 9) <= threshold]

    slice_counts: Dict[str, int] = {}
    if args.slices:
        sd = Path(args.slices)
        if not sd.is_absolute():
            sd = root / args.slices
        slice_counts = write_slices(idx, sd)

    seg_manifest: List[dict] = []
    if args.segments:
        gd = Path(args.segments)
        if not gd.is_absolute():
            gd = root / args.segments
        seg_manifest = write_segments(idx, gd, min_words=args.min_segment_words)

    applied: List[str] = []
    if args.fix:
        applied = apply_fixes(idx, findings)

    import datetime

    date = datetime.date.today().isoformat()
    md = render_markdown(idx, findings, date)
    if applied:
        md += "\n## Applied fixes\n\n" + "\n".join("- %s" % a for a in applied) + "\n"
    if seg_manifest:
        readers = 0
        for m in seg_manifest:
            readers += 1                                   # general — always
            readers += 1 if args.skeptic else 0            # skeptic — opt-in
            readers += 1 if m["tables"] else 0             # evidence
            readers += 1 if (m["equations"] or m["theory_blocks"]) else 0
        CAP = 3
        comments = readers * CAP
        verifiers = len(seg_manifest)
        agents = readers + verifiers + 2
        # ~18k tokens per reader (segment + exhibits + role file), ~55k per
        # batched verifier (its segment's comments + source lookups). Calibrated
        # against the two production runs, not guessed.
        est = readers * 18_000 + verifiers * 55_000 + 2 * 120_000
        md += "\n## Projected deep-read cost\n\n"
        md += "| | |\n|---|---:|\n"
        md += "| Segments | %d |\n" % len(seg_manifest)
        md += "| Readers (skeptic %s) | %d |\n" % ("on" if args.skeptic else "off", readers)
        md += "| Verifiers (1 per segment) | %d |\n" % verifiers
        md += "| Total agents | %d |\n" % agents
        md += "| Max comments (cap %d) | %d |\n" % (CAP, comments)
        md += "| **Projected tokens** | **%.1fM** |\n" % (est / 1e6)
        if est > 2_500_000:
            md += "\n> Over the 2.5M budget. Raise `--min-segment-words` or drop `--skeptic`.\n"
        md += "\n## Deep-read segments\n\n| Segment | File | Words | Tables | Equations |\n|---|---|---:|---|---|\n"
        md += "\n".join(
            "| %s | %s | %d | %s | %s |"
            % (m["id"], m["file"], m["words"], ", ".join(m["tables"]) or "-", ", ".join(m["equations"]) or "-")
            for m in seg_manifest
        ) + "\n"
    if slice_counts:
        md += "\n## Reasoning-layer candidates\n\n| Slice | Candidates |\n|---|---:|\n"
        md += "\n".join("| %s | %d |" % (k, v) for k, v in sorted(slice_counts.items())) + "\n"

    if args.md_out:
        out = Path(args.md_out)
        if not out.is_absolute():
            out = root / args.md_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
    if args.json_out:
        out = Path(args.json_out)
        if not out.is_absolute():
            out = root / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {"index": index_payload(idx), "findings": [f.to_dict() for f in findings]}
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if not args.quiet:
        sys.stdout.write(md)

    return 1 if any(f.severity in BLOCKING for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
