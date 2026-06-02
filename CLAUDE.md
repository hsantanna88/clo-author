# CLAUDE.MD -- ML Prescriptive Analytics for Inventory Management

<!-- HOW TO USE: Replace [BRACKETED PLACEHOLDERS] with your project info.
     Customize Beamer environments for your talk preamble.
     Keep this file under ~150 lines — Claude loads it every session.
     See the guide at https://hugosantanna.github.io/clo-author/ for full documentation. -->

**Project:** Sistema de Analítica Prescriptiva Basado en Machine Learning para la Gestión de Inventarios en el Sector Logístico del Perú
**Institution:** Universidad Peruana de Ciencias Aplicadas (UPC)
**Field:** Ingeniería de Sistemas — Operations Research & Machine Learning
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile and confirm output at the end of every task
- **Single source of truth** -- Paper `main.tex` is authoritative; talks and supplements derive from it
- **Quality gates** -- weighted aggregate score; nothing ships below 80/100; see `quality.md`
- **Worker-critic pairs** -- every creator has a paired critic; critics never edit files
- **Auto-memory** -- corrections and preferences are saved automatically via Claude Code's built-in memory system

---

## Getting Started

1. Fill in the `[BRACKETED PLACEHOLDERS]` in this file
2. Run `/discover interview [topic]` to build your research specification
3. Or run `/new-project [topic]` for the full orchestrated pipeline

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.MD                    # This file
├── .claude/                     # Rules, skills, agents, hooks
├── Bibliography_base.bib        # Centralized bibliography
├── paper/                       # Main LaTeX manuscript (source of truth)
│   ├── main.tex                 # Primary paper file
│   ├── sections/                # Section-level .tex files
│   ├── figures/                 # Generated figures (.pdf, .png)
│   ├── tables/                  # Generated tables (.tex)
│   ├── talks/                   # Beamer presentations
│   ├── quarto/                  # Quarto RevealJS presentations
│   ├── preambles/               # LaTeX headers / shared preamble
│   ├── supplementary/           # Online appendix and supplements
│   └── replication/             # Replication package for deposit
├── data/                        # Project data
│   ├── raw/                     # Original untouched data (often gitignored)
│   └── cleaned/                 # Processed datasets ready for analysis
├── scripts/                     # Analysis code (R, Python, Julia)
├── quality_reports/             # Plans, session logs, reviews, scores
├── explorations/                # Research sandbox (see rules)
├── templates/                   # Session log, quality report templates
└── master_supporting_docs/      # Reference papers and data docs
```

---

## Commands

```bash
# Paper compilation (latexmk handles multi-pass + biber automatically)
cd paper && latexmk main.tex

# Talk compilation
cd paper/talks && latexmk talk.tex

# Clean auxiliary files
cd paper && latexmk -c
```

> **Note:** `paper/latexmkrc` configures XeLaTeX, TEXINPUTS, and BIBINPUTS.
> On Overleaf, set compiler to XeLaTeX via Menu > Compiler — Overleaf reads `latexmkrc` automatically.

---

## Quality Thresholds

| Score | Gate | Applies To |
|-------|------|------------|
| 80 | Commit | Weighted aggregate (blocking) |
| 90 | PR | Weighted aggregate (blocking) |
| 95 | Submission | Aggregate + all components >= 80 |
| -- | Advisory | Talks (reported, non-blocking) |

See `quality.md` for weighted aggregation formula.

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/new-project [topic]` | Full pipeline: idea → paper (orchestrated) |
| `/discover [mode] [topic]` | Discovery: interview, literature, data, ideation |
| `/strategize [mode] [question]` | Identification strategy, pre-analysis plan, or formal theory section (`theory` mode) |
| `/analyze [dataset]` | End-to-end data analysis |
| `/write [section]` | Draft paper sections + humanizer pass (`style-guide` mode extracts voice from prior papers) |
| `/review [file/--flag]` | Quality reviews (routes by target: paper, code, peer) |
| `/revise [report]` | R&R cycle: classify + route referee comments |
| `/talk [mode] [format]` | Create, audit, or compile Beamer presentations |
| `/submit [mode]` | Journal targeting → package → audit → final gate |
| `/tools [subcommand]` | Utilities: commit, compile, validate-bib, journal, etc. |
| `/checkpoint [--flag]` | Session handoff: memory + SESSION_REPORT + research journal (+ Obsidian if configured) |

---

<!-- CUSTOMIZE: Replace the example entries below with your own
     Beamer environments for talks. -->

## Beamer Custom Environments (Talks)

| Environment       | Effect        | Use Case       |
|-------------------|---------------|----------------|
| `resultframe`     | Highlighted result box | Key findings and metrics |
| `algorithmframe`  | Algorithm pseudocode | ML pipeline steps |

---

## Output Organization

<!-- Options: by-script (default) or by-purpose -->
Output organization: by-script

<!-- by-script:  paper/figures/main_regression/figure1.pdf, paper/tables/main_regression/table1.tex -->
<!-- by-purpose: paper/figures/estimation/coefplot_main.pdf, paper/tables/robustness/alt_controls.tex -->

---

## Current Project State

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Paper | `paper/main.tex` | draft | Tesis: analítica prescriptiva ML para inventarios |
| Data | `scripts/python/` | in-progress | Comparación de algoritmos ML sobre datos de compras |
| Replication | `paper/replication/` | not started | Pendiente |
| Presentación | `paper/talks/` | -- | Pendiente |
