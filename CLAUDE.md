# CLAUDE.MD -- Empirical Economics Research with Claude Code

**Project:** The Spectre of Slavery: Newspaper Politicking During the American Civil War
**Institution:** George Mason University
**Field:** Economic History & Political Economy
**Branch:** main

------------------------------------------------------------------------

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile and confirm output at the end of every task
- **Single source of truth** -- Paper `paper/main.qmd` (Quarto) is authoritative
- **Quality gates** -- weighted aggregate score; nothing ships below 80/100; see `quality.md`
- **Worker-critic pairs** -- every creator has a paired critic; critics never edit files
- **Auto-memory** -- corrections and preferences are saved automatically via Claude Code's built-in memory system

------------------------------------------------------------------------

## Paper Format

**Quarto** (not LaTeX directly). Main file: `paper/main.qmd`

```bash
# Compile paper
quarto render paper/main.qmd

# Preview paper (live reload)
quarto preview paper/main.qmd
```

Config: `paper/_quarto.yml` | Bibliography: `paper/references.bib`
Templates: `paper/preambles/draft-article/` and `paper/preambles/beamer/`

------------------------------------------------------------------------

## Pipeline

```
Python notebooks (scripts/python/)
    text processing, BERTopic, sentiment
    --> data/cleaned/bertopic_panel_{MODEL}.csv  [gitignored, on HuggingFace]

R scripts (scripts/R/)
    01_build_panel.R    -->  data/cleaned/cong_pnl*.rds, pres_pnl*.rds
    02_event_study.R    -->  paper/figures/02_event_study/
    03_crosssection.R   -->  paper/tables/03_crosssection/
    04_mechanisms.R     -->  paper/tables/04_mechanisms/, paper/figures/04_mechanisms/

Quarto
    paper/main.qmd      -->  _output/main.pdf
```

**Column names from notebooks:**
- `cos_sim_politics`, `cos_sim_slavery_direct`, `cos_sim_slavery_ideology`
- `cos_sim_abolition`, `cos_sim_race`, `cos_sim_black_military`
- `vader_compound` (mean VADER compound per lccn-month)

**Panel structure:** `lccn x year_month` aggregated (notebooks handle article-level to panel)

**Large files:** HuggingFace repo `patrickjcrawford/civil-war-news`
- `bertopic_panel_{MODEL}.csv`, `bertopic_results_{MODEL}.csv`, `sentiment_results.csv`
- Place in `data/cleaned/` before running `01_build_panel.R`

------------------------------------------------------------------------

## Folder Structure

```
acw-newspapers/
├── CLAUDE.md
├── .claude/                     # Rules, skills, agents, hooks
├── paper/                       # Quarto manuscript (source of truth)
│   ├── main.qmd                 # Primary paper file
│   ├── _quarto.yml              # Quarto configuration
│   ├── references.bib           # Bibliography
│   ├── figures/                 # Generated figures (by-script subdirs)
│   ├── tables/                  # Generated tables (by-script subdirs)
│   ├── sections/                # Section-level .qmd files
│   ├── preambles/               # LaTeX templates for PDF output
│   └── _extensions/             # Quarto extensions
├── data/
│   ├── raw/                     # Small files committed; large gitignored
│   └── cleaned/                 # RDS panels + bertopic CSVs (gitignored)
├── scripts/
│   ├── python/                  # Jupyter notebooks (text processing pipeline)
│   └── R/                       # Regression + table scripts
├── quality_reports/             # Plans, session logs, reviews
└── master_supporting_docs/      # Reference papers and data docs
```

------------------------------------------------------------------------

## Hypotheses

| ID | Description | Script |
|----|-------------|--------|
| H1 | Slavery discourse spikes pre-election | 02_event_study.R |
| H2 | Higher cos_sim -> higher Dem vote share | 03_crosssection.R |
| H3 | Effect null/weaker for Rep vote share | 03_crosssection.R |
| H4 | cos_sim x negative sentiment amplifies H2 | 03_crosssection.R |
| H5 | Effect larger for Dem-leaning newspapers | 04_mechanisms.R |
| H6 | Spatial spillovers across county lines | 04_mechanisms.R |
| H7 | Effect holds in presidential elections | 04_mechanisms.R |
| H8 | Battle proximity attenuates effect | 04_mechanisms.R |

------------------------------------------------------------------------

## Quality Thresholds

| Score | Gate       | Applies To                        |
|-------|------------|-----------------------------------|
| 80    | Commit     | Weighted aggregate (blocking)     |
| 90    | PR         | Weighted aggregate (blocking)     |
| 95    | Submission | Aggregate + all components >= 80  |
| --    | Advisory   | Talks (reported, non-blocking)    |

------------------------------------------------------------------------

## Skills Quick Reference

| Command | What It Does |
|------------------------------|------------------------------------------|
| `/new-project [topic]` | Full pipeline: idea to paper (orchestrated) |
| `/discover [mode] [topic]` | Discovery: interview, literature, data, ideation |
| `/strategize [mode] [question]` | Identification strategy, pre-analysis plan |
| `/analyze [dataset]` | End-to-end data analysis |
| `/write [section]` | Draft paper sections + humanizer pass |
| `/review [file/--flag]` | Quality reviews |
| `/revise [report]` | R&R cycle: classify + route referee comments |
| `/talk [mode] [format]` | Create, audit, or compile presentations |
| `/submit [mode]` | Journal targeting to package to audit to final gate |
| `/checkpoint [--flag]` | Session handoff: memory + SESSION_REPORT + research journal |

------------------------------------------------------------------------

## Output Organization

Output organization: by-script

------------------------------------------------------------------------

## Current Project State

| Component | File | Status | Description |
|------------------|-------------------------------|------------|-------------------------------|
| Paper | `paper/main.qmd` | not started | Quarto manuscript skeleton |
| Panel build | `scripts/R/01_build_panel.R` | ready | Awaits bertopic_panel_*.csv |
| Event study | `scripts/R/02_event_study.R` | ready | H1 |
| Cross-section | `scripts/R/03_crosssection.R` | ready | H2 to H4 |
| Mechanisms | `scripts/R/04_mechanisms.R` | ready | H5 to H8 |
| Notebooks | `scripts/python/` | complete | 6 BERTopic pipeline notebooks |
| Replication | `paper/replication/` | not started | -- |
