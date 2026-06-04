---
name: paper-format
description: Apply and enforce the mandatory paper house style — float placement (tables/figures collected at end of main.tex), Table 1 pre-treatment characteristics, canonical threeparttable/subcaption wrappers, section order, captions. Use when building, formatting, or auditing a paper's tables, figures, or structure. Enforces INV-23/24/25.
argument-hint: "[mode: audit | scaffold | table1 | show] [target file]"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash
---

# Paper Format (House Style)

Applies and enforces the **mandatory** organization rule in `.claude/rules/paper-organization.md`
(blocking invariants **INV-23, INV-24, INV-25**). This is non-negotiable house style — every agent and
Claude must follow it. When in doubt, open the reference exemplars named in the rule.

**Input:** `$ARGUMENTS` — a mode and optional target. Default mode: `audit`.

## Modes

### `audit [main.tex]` (default)
Check a paper against the house style and report violations with invariant numbers:
1. **INV-23 — floats at end.** Grep `sections/*.tex` for `\begin{table}` / `\begin{figure}` → any hit is a violation (floats must be in `main.tex`'s end blocks, not in section files). Confirm `main.tex` has TABLES and FIGURES blocks after `\printbibliography`.
2. **INV-24 — Table 1.** Confirm the first table is pre-treatment characteristics: two group columns, thematic panels, unit counts at the bottom, and **no difference / SD / p-value column**.
3. **INV-25 — wrappers.** Every table uses `threeparttable` + `tablenotes` (or `\inputtblr` + `parbox`) with exhaustive notes; every figure uses `subcaption` with the overall `\caption{}` on top.
4. Booktabs only (no `\hline`/vertical rules), bare exhibits from scripts (INV-13), no in-figure titles (INV-12).
Report a pass/fail list; do not edit unless asked.

### `scaffold [main.tex]`
Insert the empty TABLES and FIGURES blocks at the end of `main.tex` (after the bibliography) using the
canonical comment banners, and move any inline floats from section files into those blocks.

### `table1`
Build the pre-treatment characteristics table (Table 1) from the project's panel: two group columns
(treated vs. control), thematic panels, counts at the bottom, no difference column. Export a bare
`tabular` to `tables/.../` and wrap it in `main.tex` with the canonical `threeparttable` block.

### `show`
Print the house-style templates (table wrapper, figure wrapper, Table 1 model) from the rule for quick
copy-paste.

## Authority

The full specification lives in `.claude/rules/paper-organization.md`. This skill operationalizes it; the
rule is the source of truth. Where this house style and `working-paper-format.md` disagree on float
placement, the house style wins.
