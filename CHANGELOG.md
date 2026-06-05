# Changelog

All notable changes to the Clo-Author are documented here.

**Versioning:** CalVer (YY.MM) — one version per month maximum. Git commits provide granularity within a release. Releases before 26.05 used semver tags.

------------------------------------------------------------------------

## [26.05](https://github.com/hugosantanna/clo-author/compare/v4.2.0...v4.3.0) — May 2026

### HTML Report Pipeline

Two Python generators produce self-contained interactive HTML from agent markdown output:

- **`scripts/generate_dashboard.py`** — project-level overview (manuscript sections, data, code, quality scorecard, review history, active plans)
- **`scripts/generate_html_report.py`** — 5 detail report subcommands (peer-review, code-audit, strategy-review, quality-gate, literature)

Shared design system in `templates/html/base/` (styles.css + components.js). Dark mode, print support, collapsible sections, filter engine.

### MAS Evolution v2

Five architectural phases drawn from OxyGent, LangGraph, Data-to-Paper, MAR, and Cunningham's Referee 2:

- **Permission Registry** — centralized agent registry (`permissions.md`) replacing hardcoded dispatch tables. Adding a new agent is a one-file change.
- **Lifecycle Validation** — PRE-dispatch and POST-completion handoff checks with fail-fast (`lifecycle.md`)
- **Writer Evolution** — writer-critic rebuilt with 8 categories (voice fidelity, claim-source traceability INV-22). Writer hard gates: refuses Results without tables, refuses drafting without style guide, section-level approval checkpoints.
- **Cold-Read Critics** — all 7 critics evaluate blind (no round history). Dual-critic dispatch for gate artifacts.
- **Pipeline Checkpointing** — structured JSON state (`pipeline_state.json`) survives sessions. Execution traces with Mermaid graphs.
- **Learning Loop** — post-pipeline pattern detection (HIGH-PERF, FRICTION, ESCALATION). Learning promotion after 3+ project validation.

### Skill-Centric Restructure

Skills are now rich directories — not thin dispatchers. Each skill folder contains templates, gotchas, references, and config. Agents slimmed to identity + voice + constraints only.

- **76 new template/reference/config files** across 13 skill folders
- **15 agents slimmed** (total lines: 4,454 → 1,898, −57%)
- **Three-level progressive loading:** metadata (always) → SKILL.md (on trigger) → templates (on demand)
- **Gotchas as first-class content** — every skill documents known failure points

### Session-Scoped Guards

- `/freeze [dirs]` — blocks Edit/Write outside specified directories for the session
- `/careful` — blocks destructive bash commands for the session
- `session-guard.py` PreToolUse hook enforces both; zero overhead when inactive

### Quarto-First Talks

`/talk create` now defaults to Quarto RevealJS. Beamer available via `--beamer` flag.

### Guide Site

9 pages rewritten with guide-writer voice (bold openings, problem-solution arcs, progressive disclosure). Migrated to thariqs aesthetic (ivory/clay/serif). agents.qmd compressed 603 → 205 lines. Skill-folder architecture documented. Nav reordered for user journey.

### Also

- CalVer adoption (YY.MM)
- Rewind strategy added to workflow.md
- `pre-compact.py` exit code fix (was blocking compaction)

------------------------------------------------------------------------

## [26.04.3](https://github.com/hugosantanna/clo-author/compare/v4.1.1...v4.2.0) — 2026-04-17 — Theorist Pair, Personal Style Guide, Checkpoint

Three feature additions inspired by parallel work in the Claude-Code-for-economists space (Goldsmith-Pinkham's Markus Academy series) and by a theorist pair developed in the bad-controls project. Generalized and wired into the scaffold.

### Theorist + theorist-critic pair

A first-class pair for formal theory sections — assumptions, definitions, lemmas, theorems, and proofs calibrated to top methods journals (*Econometrica*, *Journal of Econometrics*, *Quantitative Economics*, *Annals of Statistics*).

- **theorist agent** drafts identification results, consistency, asymptotic normality, influence functions, DML, bootstrap validity, test properties, and comparative-static propositions. Paper-type aware — activates for econometric methods, theory+empirics, structural identification, and methodological reduced-form papers.
- **theorist-critic** reviews through 4 sequential phases with early-stop on critical gaps: (1) triage claim type, (2) proof validity (logical, measurability, expansions, identification, asymptotic distribution), (3) assumption minimality + statement calibration + notation, (4) citations + linkage + polish. Deduction rubric: -20 per logic gap, -25 circular, -15 overclaim, etc.
- **Generalized citation anchors** — a new `Theoretical Foundational References` table in `.claude/references/domain-profile.md` parameterizes the anchor list; fallback defaults baked into the agent cover DiD, IV, RDD, DML, semiparametric efficiency, GMM, bootstrap, etc.
- **Authorship-aware calibration** — a `Paper Author Team` table in the domain profile lets the theorist-critic avoid lecturing authors on results they themselves wrote.
- Scoring: 20% weight in the aggregate when a theory section is present; renormalized otherwise.
- Activation: `/strategize theory [target]` for creation, `/review --theory [target]` for audit, conditional activation in `/new-project` Phase 2.

### Personal style guide

A `/write style-guide [paper-dir]` mode that extracts the user's writing voice from their prior papers, then feeds that voice back to the writer on every subsequent invocation.

- Discovers `.tex`/`.pdf` corpus in the target directory (default `master_supporting_docs/`)
- Strategic sampling: full intros, first two paragraphs of each major section, abstract, conclusion, 5–10 results-section paragraphs per paper
- Extracts quantitative patterns (sentence-length distribution, passive/active ratio, em dash rate) and qualitative patterns (paragraph openings, section openings, lexicon used/avoided, hedging, comparison style, citation split, tone markers)
- Self-citation check surfaces author self-citations missing from `Bibliography_base.bib`
- Writes to `.claude/references/personal-style-guide.md` with quoted examples — never invents patterns
- Writer auto-loads the guide if real content is present; voice guide overrides generic academic defaults but never INV-1..21

### Compaction discipline + scaffold-friendly `/checkpoint`

Codifies compaction hygiene and adds a project-level session-handoff skill.

- **Compaction discipline** (`workflow.md` Section 5): manual `/compact` at natural stopping points over auto-compression; 5–10 turn focused sessions; `/checkpoint` before `/compact` or session end; Session Recovery now starts at Step 0 — read recent checkpoint artifacts before the plan.
- **`/checkpoint` skill** — scaffold-friendly port:
  - Core (always on, fork-friendly): auto-memory updates, `SESSION_REPORT.md` append, `quality_reports/research_journal.md` append, git-state snapshot
  - Obsidian integration (gated): activates only when `.claude/state/obsidian-config.md` exists AND Obsidian MCP is connected; otherwise skipped silently
  - `--setup-obsidian` walks user through creating config from the example template
  - Project-level skill takes precedence over user-level one inside clo-author
- Meta-governance compliance: `.claude/state/*` gitignored, `*.example` whitelisted — fork users get the template, user-specific paths stay local

### Files touched

- Agents: `theorist.md`, `theorist-critic.md` (new); `writer.md` (style-guide loading + Style Extraction Mode)
- Rules: `agents.md`, `quality.md`, `workflow.md`
- References: `domain-profile.md` (Theoretical Foundational References + Paper Author Team), `personal-style-guide.md` (new)
- Skills: `strategize/SKILL.md` (theory mode), `review/SKILL.md` (--theory flag), `new-project/SKILL.md` (conditional dispatch), `write/SKILL.md` (style-guide mode), `checkpoint/SKILL.md` (new)
- State: `obsidian-config.md.example` (new template)
- `.gitignore`, `CLAUDE.md`

------------------------------------------------------------------------

## [26.04.2](https://github.com/hugosantanna/clo-author/compare/v4.1.0...v4.1.1) — 2026-04-11 — Modern LaTeX Stack

Modernizes the LaTeX infrastructure: automated builds, modern table engine, smart cross-references, and CI compilation. All changes are Overleaf-compatible.

### latexmk Build System

- **`paper/latexmkrc`** configures XeLaTeX, TEXINPUTS, BIBINPUTS — replaces manual 4-command build
- **`paper/talks/latexmkrc`** for talk compilation
- One command: `cd paper && latexmk main.tex` (handles multi-pass + biber automatically)
- No dot prefix (Overleaf reads `latexmkrc` automatically)
- Updated: CLAUDE.md, verifier, `/tools compile`, `/talk compile`

### tabularray

- Added `tabularray` with `booktabs` and `siunitx` libraries to reference preamble
- **Hand-written tables** use `tblr`/`talltblr` (modern key-value interface for captions, notes, rules)
- **R/Python/Julia output** continues exporting bare `tabular` wrapped with `threeparttable`
- Both approaches documented in content-standards.md with examples
- INV-1 updated to accept both `threeparttable` and `talltblr`

### cleveref

- Added `\usepackage[nameinlink]{cleveref}` after `hyperref` in reference preamble
- `\cref{fig:x}` auto-generates "Figure 1" — eliminates `Figure~\ref{}` boilerplate
- INV-10 updated: `hyperref` second-to-last, `cleveref` last
- Writer-critic deducts for missing `cleveref` (-2) and manual `\ref{}` patterns (-1 each)

### microtype Promotion

- Promoted from Recommended to Required in working-paper-format.md
- Writer-critic now deducts -2 for missing `microtype`

### GitHub Actions CI

- New `.github/workflows/compile-paper.yml` — compiles paper on push/PR to `paper/**`
- Uses `xu-cheng/latex-action@v3` with XeLaTeX
- Uploads compiled PDF as artifact

------------------------------------------------------------------------

## [26.04.1](https://github.com/hugosantanna/clo-author/compare/v4.0.0...v4.1.0) — 2026-04-09 — Enforcement Layer

Adds hard mechanical enforcement underneath the existing creative orchestration. Agents still do judgment work; the new layer catches grep-able violations before judgment is even needed. Inspired by contract-driven, grep-verified patterns from defensive engineering.

### Content Invariants

- **21 numbered non-negotiable rules** in `.claude/rules/content-invariants.md`
- Consolidates scattered rules from `content-standards.md`, `working-paper-format.md`, and coding standards into one canonical reference
- Paper (INV-1–13): threeparttable with notes, booktabs only, no ggplot titles, biblatex+biber, abstract ≤150 words, numbers match tables exactly, notation consistency, causal claims require identification
- Code (INV-14–19): set.seed at top, packages at top, no absolute paths, no growing vectors, no prohibited functions
- Talk (INV-20–21): notation matches paper, every slide claim traceable to manuscript
- writer-critic, coder-critic, storyteller-critic, verifier all updated to cite invariant numbers (e.g., "violates INV-3")

### Pre-Flight Reports

- **Strategist** must output a Pre-Strategy Report proving it read literature review, data assessment, research spec, and domain profile before designing any strategy
- **Coder** must output a Pre-Code Report proving it read strategy memo and established paper-to-code naming map before writing any code
- Both agents and both skills (`/strategize`, `/analyze`) updated with mandatory structured first output
- If an input is missing, the agent says so explicitly instead of silently assuming

### Grep-Based Linter (`/tools lint`)

- New `/tools lint [file|dir]` subcommand — mechanical pre-check for R/Python/Julia scripts
- 20 checks across R (12), Python (6), Julia (3) + shared absolute-path detection
- Patterns: `setwd()`, `rm(list=ls())`, `T`/`F`, `sapply()`, `<<-`, `attach()`, missing `set.seed()`, late `library()`, `os.chdir()`, wildcard imports, bare `except:`, prohibited packages, and more
- Portable macOS/Linux (BSD grep -E, no Perl regex required)
- `/review --code` now runs lint as Step 1 before dispatching coder-critic
- New files: `.claude/hooks/lint-scripts.sh` (linter), `.claude/hooks/post-edit-lint.sh` (hook wrapper)

### Decision Records

- ADR-style records at the two stages where real choices happen:
  - **Discovery** (`/discover interview`): why this research question over alternatives
  - **Strategy** (`/strategize`): why this identification method over alternatives
- Each record captures: what was chosen, what was rejected and why, key assumptions, what would invalidate the decision
- Shared template: `templates/decision-record.md`
- Saves to `quality_reports/decisions/`

### PostToolUse Lint Hook

- Auto-lints R/Python/Julia files on every Edit/Write operation
- Advisory (exit 0) — shows warnings immediately without blocking
- Skips `.claude/` internals
- Wired into `.claude/settings.json` as PostToolUse hook

------------------------------------------------------------------------

## [26.04](https://github.com/hugosantanna/clo-author/compare/v3.1.1...v4.0.0) — 2026-04-08 — Paper-Type Architecture

Every agent now knows whether it's working on a reduced-form, structural, theory+empirics, or descriptive paper — and adapts accordingly.

### Paper-Type Awareness (7 agents rewritten)

- **Writer** rebuilt around paragraph-level argument moves (motivation, result, mechanism, qualification). Section templates for all 4 paper types with design-specific guidance (DiD/IV/RDD/event study for reduced-form; model+estimation+counterfactuals for structural; predictions+tests for theory+empirics; construction+validation for descriptive)
- **Writer-critic** upgraded to 8 check categories including paper-type coherence, results narration quality, and design-specific completeness tables
- **Strategist** expanded from reduced-form-only to full coverage: structural estimation strategy (model specification, parameter identification, estimation method, counterfactual design), theory+empirics (testable predictions, mapping to data), descriptive/measurement (construct validity, validation plan)
- **Strategist-critic** expanded with structural checklists (model specification, parameter identification, model fit, counterfactual credibility), theory+empirics checks (prediction sharpness, test power, honesty assessment), descriptive checks (construct validity, causal language)
- **Coder** rebuilt with engineering discipline: paper-to-code naming maps, numbered script structure, function-per-file, structural estimation implementation patterns (MLE/GMM/SMM/BLP), Monte Carlo simulation structure
- **Coder-critic** expanded to 16 check categories, adding numerical discipline (float guards, CDF clamping, inverse link protection, pre-allocation), structural code checks (convergence, multiple starts), and prohibited patterns table
- **Methods-referee** expanded with paper-type-specific evaluation dimensions and scoring rubrics for each type

### Numerical Discipline (new in Coder + Coder-critic)

- Float comparison guards (no `==` on floats)
- CDF clamping to \[0, 1\], inverse link protection
- Integer literals (`1L`, `seq_len(n)`)
- Pre-allocation (no growing lists in loops)
- Bootstrap/parallel patterns with proper seed handling

### Scope: Back to Economics

- Reverted scope from "empirical social science" to economics — the pipeline's agents, rules, and section templates are built for economics and that's what they should claim
- Other fields (finance, accounting, marketing, management) can adapt by customizing the domain profile and journal profiles
- Non-economics journal profiles retained — they're useful reference data for adjacent fields that use similar methods

### Profile-Aware Table Standards

- Significance stars are now journal-dependent, not hardcoded
- AEA journals (AER, AEJ:Applied, AEJ:Policy, AER:Insights): no significance stars per current AEA style guide
- All other journals: stars acceptable (default for working papers)
- Journal profiles now include `Table format` field for overrides

### Working Paper Format: Required vs. Recommended

- Split "Key Design Decisions" table into Required (blocking) and Recommended (advisory)
- Required: document class, margins, double-spacing, biblatex+biber, booktabs, hyperref last
- Recommended: lmodern, microtype, citation color, captionsetup, hidelinks
- Writer-critic deductions adjusted: recommended items are advisory, not blocking

### Compilation Alignment

- Fixed bibtex→biber mismatch: CLAUDE.md and tools/SKILL.md now match working-paper-format.md
- Fixed remaining uppercase paths in tools/SKILL.md (Paper→paper, Talks→paper/talks, Preambles→preambles)

### Dead Code Removal

- Deleted `scripts/quality_score.py` (761 lines targeting nonexistent Quarto/Slides/ directories)
- Deleted `scripts/sync_to_docs.sh` (92 lines targeting nonexistent deployment structure)
- Removed stale `sync_to_docs.sh` permissions from settings.json
- Added `biber` permission to settings.json

### README Honesty

- "turns your terminal into a research assistant" → "scaffold for empirical economics research"
- "works autonomously" → removed; describes the plan-approve-review loop
- "Realistic Peer Review Simulation" → "Simulated Peer Review"
- "calibrated referee pools" → "configured referee pools"
- Dropped unverifiable "71% fewer tokens" claim
- Added Limitations section

------------------------------------------------------------------------

## [26.03.6](https://github.com/hugosantanna/clo-author/compare/v3.1.0...v3.1.1) — 2026-03-24

### Output Organization

- Added `Output Organization` setting to CLAUDE.md (by-script or by-purpose)
- Default is **by-script**: outputs go to subfolders named after the generating script (e.g., `paper/figures/main_regression/figure1.pdf`)
- Coder agent reads this setting and follows accordingly

### Bug Fixes

- Fixed Paper/ → paper/ rename on case-insensitive macOS filesystem (git index mismatch)
- Fixed all stale uppercase paths across 10 files (agents, skills, rules, CLAUDE.md)
- Fixed broken domain-profile path in /new-project
- Added plan mode (Step 0) to /new-project
- Removed stale upstream remote to Pedro's repo

------------------------------------------------------------------------

## [26.03.5](https://github.com/hugosantanna/clo-author/compare/v3.0.0...v3.1.0) — 2026-03-23

### Skill Detail Restoration — 26.02.1 Depth Returns to 26.03.4

The 26.03 to 26.03.4 consolidation accidentally stripped practical detail from 6 skills. This release restores all 22 lost items while keeping the 26.03.4 structure.

**`/discover`:** - Restored proximity scoring (1-5 scale) for literature papers - Restored citation chains as explicit search vector (forward + backward) - Restored feasibility grades (A/B/C/D) for datasets - Restored data rejection table format - Restored 5-point explorer-critic data critique (measurement validity, sample selection, external validity, identification compatibility, known issues) - Restored `% UNVERIFIED` citation marking convention

**`/strategize`:** - Restored interactive PAP interview (6-question guided flow) - Restored platform-specific PAP templates (AEA RCT Registry, OSF, EGAP) - Restored observational study PAP adaptation protocol - Restored optional strategist-critic review after PAP creation - Restored `[ASSUMED]` placeholder safety flags with pre-registration checklist

**`/analyze`:** - Restored R script skeleton template (6-section structure) - Restored `results_summary.md` as mandatory artifact (handoff to writer) - Restored full 12-category code review checklist (explicit categories 1-12) - Restored saveRDS serialization guidance - Restored Scott Cunningham replication tolerance thresholds for `--dual` mode

**`/review`:** - Restored 4-phase econometrics protocol (claim → validity → inference → polish) - Restored early stopping rule (CRITICAL Phase 2 issues → focus there) - Restored severity calibration examples (9 examples with Major/Minor ratings) - Restored Verifier pass/fail definition (paper, code, replication package) - Restored "design-opinionated, package-flexible" principle

**`/write`:** - Restored 7-item context gathering checklist - Restored quality self-check before presenting (7 items) - Restored TBD/VERIFY/PLACEHOLDER flagging system - Restored LaTeX conventions (`\citet` vs `\citep`, booktabs, notation protocol)

**`/talk`:** - Restored "figures over tables; tables in backup" design principle - Restored 5-category review detail with full descriptions - Restored audience calibration principle

### Referee Pet Peeves Expansion

- **27 critical pet peeves** (was 12) — added Oster bounds, leave-one-out, power obsession, balance tables, ML variable selection, first-stage F, Bonferroni, and more
- **24 constructive pet peeves** (was 12) — added event study appreciation, null result honesty, institutional detail, code availability, brevity rewards, contradictory findings engagement, and more
- More variety = less predictable referees = more realistic simulation

------------------------------------------------------------------------

## [26.03.4](https://github.com/hugosantanna/clo-author/compare/v2.0.3...v3.0.0) — 2026-03-20

### Scope Clarification

- clo-author is built for empirical economics; adaptable to adjacent fields (finance, accounting, marketing, management) via domain profile
- Updated meta-governance to reflect this scope
- Institution updated from Emory to UAB

### Peer Review Simulation — Complete Redesign

- **New `editor` agent** — desk reviews papers before sending to referees, verifies novelty claims via WebSearch, selects referee dispositions based on journal culture, makes independent editorial decisions (not score averaging)
- **Referee dispositions** — 6 intellectual priors (Structuralist, Credibility, Measurement, Policy, Theory, Skeptic) assigned by the editor based on journal culture
- **Referee pet peeves** — each referee gets 1 critical and 1 constructive pet peeve, creating realistic variation across reviews
- **Journal-driven referee selection** — new `Referee pool` field in journal profiles weights which dispositions the editor draws from (e.g., Econometrica skews Structuralist/Theory, QJE skews Credibility/Policy)
- **"What would change my mind"** — every major referee comment must include specific evidence or analysis that would resolve the concern
- **Desk reject** — editor can reject without sending to referees (wrong fit, no contribution, already published)
- **FATAL/ADDRESSABLE/TASTE classification** — editorial decisions classify each concern, producing MUST/SHOULD/MAY action items
- **R&R memory** — `--r2` flag reloads prior referee reports; referees check whether each concern was addressed (Resolved/Partially/Not addressed)
- **Round escalation** — Round 2 allows Major Revisions if new issues surface; Round 3 is Accept/Minor/Reject only; max 3 rounds
- **Hostile stress test** — `--stress [journal]` assigns adversarial dispositions, doubles critical pet peeves, pre-submission battle testing
- **Literature verification** — editor uses WebSearch during desk review to verify novelty claims against published work

### Journal Profiles Expansion

- Added 15 new A\* journal profiles across 4 fields:
  - **Finance:** JF, JFE, RFS, JFQA
  - **Accounting:** JAR, JAE, TAR, CAR
  - **Marketing:** JMR, Marketing Science, JCR
  - **Management:** Management Science, SMJ, ASQ
- All profiles include `Referee pool` disposition weights calibrated to each journal's review culture
- Journal profiles moved from rules to `.claude/references/` — loaded on demand, zero per-session overhead

### Context Reduction: 66% Less Per-Session Overhead

- **Before:** \~3,518 lines of rules loaded every session
- **After:** \~1,198 lines loaded per session
- Deleted `archive/` directory (22 duplicate rule files, \~1,769 lines)
- Trimmed `meta-governance.md` from 252 to 20 lines
- Moved `journal-profiles.md` to on-demand reference (299 lines saved per session)
- Merged `tables.md` and `figures.md` into path-scoped `content-standards.md`

### Content Standards Improvements

- Added figure standards: PDF vector output, colorblind-friendly palettes, grayscale independence (shape + linetype redundancy), figure width guidance
- Restored `threeparttable` requirement for tables (lost in prior merge)
- Consolidated all content rules in one path-scoped file
- Added 5 table type templates: descriptive statistics, regression results, multi-outcome panels, balance tables, robustness

### Folder Structure Reorganization

- Figures, tables, talks, and Quarto presentations now live inside `Paper/` (self-contained paper directory)
- Added `Data/raw/` and `Data/cleaned/` directories
- Deleted `Slides/` (legacy from lecture workflow)
- Quarto RevealJS presentation support added (`/talk create [format] --quarto`)

### Other Changes

- Replaced `[LEARN]` tags with Claude Code's built-in auto-memory system
- Added `[YOUR FIELD]` placeholder to CLAUDE.md and starter prompt
- Agent prompts made field-neutral — read field from `.claude/references/domain-profile.md` (defaults to economics)
- Deleted archived agents (16 files) and archived skills (20+ files)
- Guide and documentation fully updated for 26.03.4

------------------------------------------------------------------------

## [26.03.3](https://github.com/hugosantanna/clo-author/compare/v2.0.2...v2.0.3) — 2026-03-07

### Working Paper Format Rule

- **`working-paper-format.md`** — new always-on rule: enforces standard economics working paper format (12pt article, 1in margins, double-spaced body, single-spaced abstract, `titling` package for proper title/author font sizes, `\quad` author spacing, `booktabs` tables, `threeparttable` notes, `aer` bibliography style)
- Writer-critic deduction rubric included (e.g., -5 for wrong document class, -3 for `\textbf{}` on title, -5 for missing JEL codes)
- Ensures title page fits on one page: title + authors + abstract + JEL + keywords

------------------------------------------------------------------------

## [26.03.2](https://github.com/hugosantanna/clo-author/compare/v2.0.1...v2.0.2) — 2026-03-07

### Figures & Tables Rules

- **`figures.md`** — new always-on rule: no embedded ggplot titles, descriptive filenames, LaTeX `\caption{}` as authoritative title, serif fonts, publication-quality axis labels, show all years on x-axis (≤20 ticks)
- **`tables.md`** — new always-on rule: no embedded titles in generated `.tex` files, `threeparttable` + `booktabs`, notes in paper not R output
- These complement `content-standards.md` (path-scoped, comprehensive) with concise always-on reminders

------------------------------------------------------------------------

## [26.03.1](https://github.com/hugosantanna/clo-author/compare/v2.0.0...v2.0.1) — 2026-03-05

### Cross-Language Replication

- **`/analyze --dual r,python`** — run the same analysis in two languages in parallel, compare results within tolerance
- **`/review --replicate python`** — re-implement existing code in a different language, compare outputs
- Both use `domain-profile.md` Quality Tolerance Thresholds for pass/fail
- Coder agent updated with cross-language replication mode and common divergence sources
- Inspired by Scott Cunningham's approach to cross-language validation

------------------------------------------------------------------------

## [26.03](https://github.com/hugosantanna/clo-author/compare/v1.0.1...v2.0.0) — 2026-03-05

**The Great Restructure.** 16-agent worker-critic system, journal-calibrated referees, consolidated rules, 6-page guide with command reference dictionary.

### Architecture

- **16 specialized agents** in 7 worker-critic pairs + 2 blind referees + orchestrator + verifier
- **New agents:** data-engineer, coder-critic, writer-critic, strategist-critic, librarian-critic, explorer-critic, storyteller-critic, domain-referee, methods-referee
- **Retired agents:** Debugger, Proofreader, Econometrician, Editor, Surveyor, Discussant, Referee (replaced by specialized critic/referee counterparts)
- Worker-critic separation of powers: critics never edit files, creators never self-score

### Journal-Calibrated Peer Review

- `/review --peer JHR` makes referees emulate that journal's review culture
- 15 pre-populated journal profiles (Top-5 + top field + strong field)
- 3-tier fallback: pre-populated → unknown journal + domain profile → user-added custom
- Custom template at bottom of `journal-profiles.md` for adding your own journals

### Skills Consolidation

- **10 slash commands** (down from 20+), each with flags/modes instead of separate skills
- `/discover` replaces `/lit-review`, `/find-data`, `/research-ideation`, `/interview-me`
- `/review` replaces `/review-paper`, `/review-r`, `/econometrics-check`, `/proofread`, `/visual-audit`
- `/write` replaces `/draft-paper`, `/humanizer`
- `/talk` replaces `/create-talk`, `/compile-latex` (for talks)
- `/submit` replaces `/target-journal`, `/data-deposit`, `/audit-replication`, `/deploy`
- `/tools` replaces `/commit`, `/compile-latex`, `/validate-bib`, `/journal`, `/context-status`, `/learn`
- `/revise` replaces `/respond-to-referee`
- `/strategize` replaces `/identify`, `/pre-analysis-plan`
- `/analyze` replaces `/data-analysis`

### Rules Consolidation

- 18 single-topic rule files → 5 consolidated files:
  - `agents.md` — pairing, separation of powers, escalation
  - `workflow.md` — planning, orchestration, dependencies, standalone access
  - `quality.md` — scoring, thresholds, severity gradient
  - `logging.md` — sessions, reports, research journal
  - `content-standards.md` — writing, coding, formatting
- Old rule files archived to `.claude/rules/archive/`
- New: `journal-profiles.md` — 15 economics journal review profiles

### Guide Website

- **6 pages** (up from 3): Quick Start, User Guide, Agents, Architecture, Customization, Reference
- New **Command Reference** page: every command, flag, and subcommand in one scannable page
- New **Meet the Agents** page: all 16 agents with roles, what they create/check
- New **Customization Guide**: domain profile, journal profiles, rules, skills, agents, hooks
- Pipeline diagram with backward arrows (Peer Review → Discovery/Strategy/Execution)
- Cyberpunk neon theme throughout all Mermaid diagrams

### Other

- Pipeline diagram shows 3 feedback loops from Peer Review (missing lit, flawed ID, more checks)
- Archived old skills, agents, hooks, and rules (preserved in `archive/` directories)
- Updated README.md with 16-agent table and 10-command reference

------------------------------------------------------------------------

## [26.02.2](https://github.com/hugosantanna/clo-author/compare/v1.0.0...v1.0.1) — 2026-02-25–26

### Adversarial Architecture

- Worker-critic pairing: every creator has a paired reviewer
- Separation of powers: critics can't edit, creators can't self-score
- Three-strikes escalation protocol
- Dependency-driven orchestration (phases activate by dependency, not sequence)
- Cyberpunk neon theme for guide website
- 3-page Quarto website: Quick Start, User Guide, Architecture
- Reoriented from lecture production to applied econometrics research

------------------------------------------------------------------------

## [26.02.1](https://github.com/hugosantanna/clo-author/compare/v0.1.0...v1.0.0) — 2026-02-08–15

### Research Workflow

- Research skills: `/lit-review`, `/find-data`, `/identify`, `/draft-paper`, `/review-paper`
- Smart hooks: pre-compact context survival, post-session logging
- Skill creation template and two-tier memory system (MEMORY.md + personal)
- Meta-governance: dual nature of repo (working project + public template)
- Requirements specification phase with MUST/SHOULD/MAY framework
- Constitutional governance template

### Infrastructure

- Orchestrator/contractor protocol with dependency graph
- Plan-first workflow with context preservation
- Quality gates: 80 (commit), 90 (PR), 95 (submission)
- Figure and table generator rules (AER/QJE/Econometrica standards)
- Claude Pilot features integration

------------------------------------------------------------------------

## [26.02](https://github.com/hugosantanna/clo-author/commits/v0.1.0) — 2026-02-06–07

### Initial Release

- Forked from [Pedro Sant'Anna's claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)
- Plan-first workflow, context preservation, session logging
- Contractor/orchestrator protocol
- Hooks, MEMORY.md, responsive guide
- Parallel agents pattern, `/commit` skill
- Fork-first onboarding flow

------------------------------------------------------------------------

```{=html}
<!-- Note: Releases before 26.05 used semver git tags. Comparison links below
     reference those original tags, which remain in the repository. -->
```