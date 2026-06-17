# CLAUDE.MD -- Empirical Economics Research with Claude Code

**Project:** [PROJECT NAME]
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

------------------------------------------------------------------------

## Pipeline

Update this section to reflect your project's analysis pipeline. Example:

```
Python notebooks (scripts/python/) OR R scripts (scripts/R/)
    text/data processing
    --> data/cleaned/

R scripts (scripts/R/)
    01_build_panel.R  -->  data/cleaned/*.rds
    02_analysis.R     -->  paper/figures/02_analysis/, paper/tables/02_analysis/

Quarto
    paper/main.qmd    -->  _output/main.pdf
```

------------------------------------------------------------------------

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.md
├── .claude/                     # Rules, skills, agents, hooks
├── paper/                       # Quarto manuscript (source of truth)
│   ├── main.qmd                 # Primary paper file
│   ├── _quarto.yml              # Quarto configuration
│   ├── references.bib           # Bibliography
│   ├── figures/                 # Generated figures (by-script subdirs)
│   ├── tables/                  # Generated tables (by-script subdirs)
│   ├── sections/                # Section-level .qmd files (optional)
│   ├── preambles/               # LaTeX templates for PDF output
│   ├── talks/                   # Presentation slides (.qmd → Beamer or RevealJS)
│   └── outreach/                # Public-facing writing (op-eds, ProMarket, press)
├── data/
│   ├── raw/                     # Original data (large files gitignored)
│   └── cleaned/                 # Analysis-ready datasets (gitignored)
├── scripts/
│   ├── python/                  # Python/notebook scripts
│   └── R/                       # R analysis scripts
├── quality_reports/             # Plans, session logs, reviews
├── explorations/                # Research sandbox
└── master_supporting_docs/      # Reference papers and data docs
```

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

## Beamer Custom Environments (Talks)

| Environment  | Effect          | Use Case        |
|--------------|-----------------|-----------------|
| `[your-env]` | [Description]   | [When to use]   |

------------------------------------------------------------------------

## Output Organization

Output organization: by-script

------------------------------------------------------------------------

## Current Project State

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Paper | `paper/main.qmd` | not started | [Brief description] |
| Data | `scripts/R/` | not started | [Analysis description] |
| Replication | `paper/replication/` | not started | -- |
