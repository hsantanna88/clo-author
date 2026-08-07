# Permission Registry: Agent Capabilities and Dependencies

Every agent's capabilities, dependencies, and routing are declared here. The Orchestrator reads this file to determine dispatch rules, dependency graph, escalation routing, and quality weights. No other file hardcodes these relationships.

Adding a new agent: create the agent file in `.claude/agents/`, add an entry here. No other file needs to change.

---

## librarian
- **PHASE:** Discovery
- **PARALLEL_GROUP:** discovery
- **REQUIRES:** Research idea or research spec
- **PRODUCES:** `quality_reports/literature/{project}/`
  - Required files: `annotated_bibliography.md`, `references.bib`, `frontier_map.md`, `positioning.md`
- **CRITIC:** librarian-critic
- **ESCALATION_TARGET:** User — scope disagreement, user decides breadth vs. depth
- **QUALITY_WEIGHT:** 10% (literature coverage)

## explorer
- **PHASE:** Discovery
- **PARALLEL_GROUP:** discovery
- **REQUIRES:** Research idea or research spec
- **PRODUCES:** `quality_reports/data-assessment/{project}/`
  - Required files: `data_sources.md`, `data_dictionary.md`, `access_instructions.md`
- **CRITIC:** explorer-critic
- **ESCALATION_TARGET:** User — data feasibility deadlock, user decides resource trade-offs
- **QUALITY_WEIGHT:** 10% (data quality)

## strategist
- **PHASE:** Strategy
- **PARALLEL_GROUP:** strategy
- **REQUIRES:** `quality_reports/literature/{project}/` OR `quality_reports/data-assessment/{project}/`
- **PRODUCES:** `quality_reports/strategy/{project}/`
  - Required files: `strategy_memo.md`
  - Required sections: Estimand, Specification, Assumptions, Robustness Plan, Threats
- **CRITIC:** strategist-critic
- **ESCALATION_TARGET:** User — fundamental design question, needs human judgment
- **QUALITY_WEIGHT:** 25% (identification validity)

## theorist
- **PHASE:** Strategy
- **PARALLEL_GROUP:** strategy
- **REQUIRES:** `quality_reports/strategy/{project}/strategy_memo.md`
- **PRODUCES:** `quality_reports/theory/{project}/`
  - Required files: `theory_memo.md`, `assumptions.tex`, `results.tex`, `proofs.tex`, `notation_glossary.md`
- **CRITIC:** theorist-critic
- **ESCALATION_TARGET:** User — proof-level disagreement, user adjudicates whether the result holds
- **QUALITY_WEIGHT:** 20% (theory, when present)
- **CONDITIONAL:** Only for paper types with formal theory: econometric methods, theory+empirics, structural identification, methodological reduced-form. Excluded and weight renormalized for applied papers using off-the-shelf estimators.

## data-engineer
- **PHASE:** Execution
- **PARALLEL_GROUP:** execution-data
- **REQUIRES:** `quality_reports/strategy/{project}/strategy_memo.md` AND strategist-critic score >= 80
- **PRODUCES:** `data/cleaned/`, `paper/figures/` (data visualization), data codebooks
- **CRITIC:** coder-critic
- **ESCALATION_TARGET:** strategist-critic — re-evaluates whether the data specification is tractable
- **QUALITY_WEIGHT:** Included in code quality weight (not scored separately)

## coder
- **PHASE:** Execution
- **PARALLEL_GROUP:** execution-code
- **REQUIRES:** `quality_reports/strategy/{project}/strategy_memo.md` AND strategist-critic score >= 80
- **PRODUCES:** `scripts/`, `paper/tables/`, `paper/figures/`, `quality_reports/results_summary.md`
- **CRITIC:** coder-critic
- **ESCALATION_TARGET:** strategist-critic — re-evaluates whether the strategy memo is implementable
- **QUALITY_WEIGHT:** 15% (code quality)

## explainer
- **PHASE:** Execution
- **PARALLEL_GROUP:** execution-explain
- **REQUIRES:** `scripts/` contains the target script AND coder-critic score >= 80
- **PRODUCES:** `quality_reports/explainers/`
  - Required files: `{script}_explainer.md`, `{script}_quiz.md`, `{script}_quiz_key.md`
  - Required sections (explainer): Headline, Sample construction ledger, Variable construction, Judgment calls, What would change the answer, Open questions
- **CRITIC:** None — the quiz is the verification, and the author is who it verifies
- **ESCALATION_TARGET:** coder — the sample ledger came back `NOT INSTRUMENTED`, so the script must print drop counts before an honest explainer can exist
- **QUALITY_WEIGHT:** None. Understanding is a gate, not a score (see `.claude/rules/understanding.md`) — a quiz result is a fact about the author, not the artifact.

## writer
- **PHASE:** Execution
- **PARALLEL_GROUP:** execution-write
- **REQUIRES:** coder-critic score >= 80 AND `paper/tables/` contains `.tex` files
- **PRODUCES:** `paper/main.tex`, `paper/sections/*.tex`, `quality_reports/claim_source_map_{project}.md`
- **CRITIC:** writer-critic
- **ESCALATION_TARGET:** Orchestrator — structural rewrite, not just polish
- **QUALITY_WEIGHT:** 10% (manuscript polish)

## editor
- **PHASE:** Peer Review
- **PARALLEL_GROUP:** peer-review
- **REQUIRES:** writer-critic score >= 80 AND coder-critic score >= 80
- **PRODUCES:** `quality_reports/reviews/editorial_decision.md`
  - Dispatches domain-referee and methods-referee (see below)
  - Synthesizes referee reports into editorial decision
- **CRITIC:** None — the editor IS the review coordinator
- **ESCALATION_TARGET:** User — editorial judgment calls
- **QUALITY_WEIGHT:** None (manages the peer review process, not scored directly)

## domain-referee
- **PHASE:** Peer Review
- **PARALLEL_GROUP:** peer-review
- **REQUIRES:** writer-critic score >= 80 AND coder-critic score >= 80
- **PRODUCES:** `quality_reports/reviews/{project}_referee_domain.md`
- **CRITIC:** None — referee is already a reviewer
- **ESCALATION_TARGET:** editor
- **QUALITY_WEIGHT:** 12.5% (half of 25% paper quality)

## methods-referee
- **PHASE:** Peer Review
- **PARALLEL_GROUP:** peer-review
- **REQUIRES:** writer-critic score >= 80 AND coder-critic score >= 80
- **PRODUCES:** `quality_reports/reviews/{project}_referee_methods.md`
- **CRITIC:** None — referee is already a reviewer
- **ESCALATION_TARGET:** editor
- **QUALITY_WEIGHT:** 12.5% (half of 25% paper quality)

## storyteller
- **PHASE:** Presentation
- **PARALLEL_GROUP:** presentation
- **REQUIRES:** writer-critic score >= 80
- **PRODUCES:** `paper/talks/` or `paper/quarto/`
- **CRITIC:** storyteller-critic
- **ESCALATION_TARGET:** Writer — talk narrative issues stem from paper structure
- **QUALITY_WEIGHT:** Advisory (reported, non-blocking)

## coherence-specification / coherence-claims / coherence-continuity / coherence-notation / coherence-theory
- **PHASE:** Any — runs standalone wherever a manuscript exists
- **PARALLEL_GROUP:** coherence-finders (all five dispatch concurrently)
- **REQUIRES:** `quality_reports/coherence/slices/{name}.json`, produced by `scripts/paper_coherence.py --slices`
- **PRODUCES:** candidate findings (JSON, in-memory) — no files
- **CRITIC:** coherence-skeptic — one instance per candidate finding, prompted to refute
- **ESCALATION_TARGET:** coherence-consolidator
- **QUALITY_WEIGHT:** None — advisory layer, never blocks
- **CONDITIONAL:** Each agent is skipped when its slice is empty. `coherence-theory` produces nothing on applied papers using off-the-shelf estimators, which is the correct result.

## coherence-skeptic
- **PHASE:** Any
- **PARALLEL_GROUP:** coherence-verify (one instance per candidate finding)
- **REQUIRES:** One candidate finding from a coherence finder
- **PRODUCES:** A refutation verdict, optionally a corrected finding
- **CRITIC:** None — this agent *is* the verification step
- **ESCALATION_TARGET:** coherence-consolidator
- **QUALITY_WEIGHT:** None
- **NOTE:** Defaults to refuted when uncertain. Fan-out multiplies the false-positive surface; this stage is what pays for it.

## coherence-consolidator
- **PHASE:** Any
- **PARALLEL_GROUP:** None — single merge stage, runs after the fan-out barrier
- **REQUIRES:** Surviving findings from all finders, plus the Layer 1 deterministic findings
- **PRODUCES:** `## Reasoning layer` section appended to `quality_reports/coherence/YYYY-MM-DD_report.md`
  - Required content: funnel counts (candidates → survived → merged), ranked findings
- **CRITIC:** None — infrastructure agent
- **ESCALATION_TARGET:** User — prose and table disagree and only the author knows which is stale
- **QUALITY_WEIGHT:** None. Coherence is a gate, not a score: Layer 1 findings block at zero tolerance rather than deducting points; reasoning findings never block.

## verifier
- **PHASE:** Submission
- **PARALLEL_GROUP:** submission
- **REQUIRES:** Overall score >= 95 AND all components >= 80
- **PRODUCES:** `quality_reports/verification_report.md`
- **CRITIC:** None — infrastructure agent
- **ESCALATION_TARGET:** User
- **QUALITY_WEIGHT:** 5% (replication readiness, 0 or 100)

---

## Parallel Groups

Agents in the same parallel group can run concurrently when their REQUIRES are met:

| Group | Agents | When |
|-------|--------|------|
| discovery | librarian, explorer | From the start (only needs research idea) |
| strategy | strategist, theorist | After Discovery (literature OR data assessment) |
| execution-data | data-engineer | After Strategy (approved strategy memo) |
| execution-code | coder | After Strategy (approved strategy memo) |
| execution-explain | explainer | After Code (approved code output) — parallel with execution-write |
| execution-write | writer | After Code (approved code output) |
| peer-review | editor, domain-referee, methods-referee | After Execution (approved paper + code) |
| presentation | storyteller | After Write (approved paper) — can run parallel with Peer Review |
| submission | verifier | After Peer Review (editorial accept/minor + overall >= 95) |

## Phase Order

```
Discovery → Strategy → Execution → Peer Review → Submission
                                         ↕
                                   Presentation (parallel)
```

Re-entry is allowed for all phases except Submission (terminal). A referee comment can trigger re-entry at any prior phase.
