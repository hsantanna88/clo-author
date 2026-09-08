# Literature Review: 6 Check Categories

Extracted from `librarian-critic.md`. Used by the librarian-critic agent for literature assessment review.

---

## 1. Coverage Gaps

- Missing subfields or adjacent literatures
- Missing seminal papers in the field
- Missing methods literature (control theory and RL foundations for the approach)

---

## 2. Venue Quality

- Over-reliance on preprints (>50% unpublished). Note: in RL-for-control a high arXiv share is
  normal and expected — flag it only when the peer-reviewed control literature is absent
- Missing papers from the core control venues (IEEE TCST, Automatica, Control Engineering
  Practice, Journal of Process Control, ISA Transactions) and from the ML venues where
  RL-for-control appears (NeurIPS, ICML, ICLR, L4DC, CDC, ACC)
- Appropriate mix of foundational and recent work

---

## 3. Scope Calibration

- Too narrow (single subfield, missing connections)?
- Too broad (unfocused, no clear positioning)?
- Right depth for the paper's contribution?

---

## 4. Recency

- Missing papers from last 2 years
- Scooping risks identified?
- Working paper versions vs. published versions

---

## 5. Categorization Quality

- Proximity scores reasonable, and on the correct scale?
  **1 = directly competes ... 5 = tangential.** Flag any use of the inverted scale
- Literature organized in a way that supports the paper's argument?
- Frontier map accurately identifies gaps?

---

## 6. BibTeX Completeness and Honesty

- All papers have BibTeX entries
- Entries are complete (venue, year, volume, pages, DOI where available)
- No duplicate keys or mismatched entries
- **Fabrication check — the heaviest deduction in this rubric.** Spot-check entries against what
  the report claims was consulted. Any citation whose details were invented rather than verified
  is a critical finding, not a minor one (INV-28)
- Unverified fields are marked `% UNVERIFIED` with a note saying which field is unconfirmed
- Claims about a paper's findings match what the librarian says it actually read (abstract vs.
  full text vs. search-result snippet)

---

## Report Format

```markdown
# Literature Review -- librarian-critic
**Date:** [YYYY-MM-DD]
**Score:** [XX/100]

## Issues Found
[Per-issue with severity and deduction]

## Score Breakdown
- Starting: 100
- [Deductions]
- **Final: XX/100**
```
