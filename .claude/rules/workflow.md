# Workflow: Planning, Orchestration, and Dependencies

---

## 1. Plan-First Protocol

**For any non-trivial task, enter plan mode before writing code.**

### The Protocol

1. **Enter Plan Mode** — use `EnterPlanMode`
2. **Check MEMORY.md** — read any `[LEARN]` entries relevant to this task
3. **Requirements Specification (for complex/ambiguous tasks)** — see below
4. **Draft the plan** — what changes, which files, in what order
5. **Save to disk** — write to `quality_reports/plans/YYYY-MM-DD_short-description.md`
6. **Present to user** — wait for approval
7. **Exit plan mode** — only after approval
8. **Save initial session log** — capture goal and key context while fresh
9. **Implement via orchestrator** — see Section 2

### Requirements Specification (For Complex/Ambiguous Tasks)

**When to use:**
- Task is high-level or vague ("improve the lecture", "analyze the data")
- Multiple valid interpretations exist
- Significant effort required (>1 hour or >3 files)

**When to skip:**
- Task is clear and specific ("fix typo in line 42")
- Simple single-file edit
- User has already provided detailed requirements

**Protocol:**
1. Use AskUserQuestion to clarify ambiguities (max 3-5 questions)
2. Create `quality_reports/specs/YYYY-MM-DD_description.md` using `templates/requirements-spec.md`
3. Mark each requirement:
   - **MUST** (non-negotiable)
   - **SHOULD** (preferred)
   - **MAY** (optional)
4. Declare clarity status for each major aspect:
   - **CLEAR:** Fully specified
   - **ASSUMED:** Reasonable assumption (user can override)
   - **BLOCKED:** Cannot proceed until answered
5. Get user approval on spec
6. THEN proceed to Step 4 (draft the plan) with spec as input

**Template:** `templates/requirements-spec.md`

**Why this helps:** Catches ambiguity BEFORE planning. Reduces mid-plan pivots by 30-50%.

### Plans on Disk

Plans survive context compression. Save every plan to:

```
quality_reports/plans/YYYY-MM-DD_short-description.md
```

Format: Status (DRAFT/APPROVED/COMPLETED), approach, files to modify, verification steps.

---

## 2. The Orchestrator Loop

**After a plan is approved, the orchestrator takes over autonomously.**

### The Dependency-Driven Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IDENTIFY — Check dependency graph, determine which phases can activate
  │
  Step 2: DISPATCH — Launch worker agents (parallel when independent)
  │         Each worker paired with its critic (see agents.md)
  │
  Step 3: REVIEW — Critic evaluates worker output, produces score
  │         If score < 80 → worker fixes → critic re-reviews (max 3 rounds)
  │         If 3 rounds fail → ESCALATE (see agents.md)
  │
  Step 4: VERIFY — Compile, render, run code, check outputs
  │         If verification fails → fix → re-verify (max 2 attempts)
  │
  Step 5: SCORE — Aggregate scores across components (see quality.md)
  │
  └── Score >= threshold?
        YES → Present summary to user
        NO  → Identify blocking components, loop back to Step 2
              After max 5 overall rounds → present with remaining issues
```

### Agent Dispatch Rules

The Orchestrator selects agents by reading `.claude/rules/permissions.md`. Each agent entry declares its PHASE, REQUIRES, and PARALLEL_GROUP. The Orchestrator matches the task to the appropriate PHASE and dispatches the agents whose REQUIRES are satisfied. Before dispatch, it runs PRE-validation per `.claude/rules/lifecycle.md`.

### Parallel Dispatch

Agents in the same PARALLEL_GROUP run concurrently when their REQUIRES are met. See `permissions.md` for the complete parallel group table.

### Limits

- **Worker-critic pairs:** max 3 rounds (then escalate)
- **Overall loop:** max 5 rounds
- **Verification retries:** max 2 attempts
- Never loop indefinitely

### Simplified Mode (R Scripts / Explorations)

For standalone R scripts, simulations, and explorations — use the simplified loop:

```
Plan approved → implement → run code → check outputs → score → done
```

No multi-agent reviews. Just: write, test, verify quality >= 80.

**Verification Checklist (Simplified):**
- [ ] Script runs without errors
- [ ] All packages loaded at top
- [ ] No hardcoded absolute paths
- [ ] `set.seed()` once at top if stochastic
- [ ] Output files created at expected paths
- [ ] Quality score >= 80

### "Just Do It" Mode

When user says "just do it" / "handle it":
- Skip final approval pause
- Auto-commit if score >= 80
- Still run the full verify-review-fix loop
- Still present the summary

---

## 3. Dependency Graph

**Phases activate by dependency, not sequence. Research is not a waterfall.**

### Phase Dependencies

Phase dependencies are declared in `.claude/rules/permissions.md`. Each agent's REQUIRES field specifies what must exist before it can be dispatched. The PHASE field determines sequencing. The PARALLEL_GROUP field determines which agents can run concurrently.

Re-entry is allowed for all phases except Submission (terminal).

### How It Works

The Orchestrator reads `permissions.md` before dispatching any agent. If an agent's REQUIRES are satisfied, it can activate — regardless of whether earlier phases are "complete."

**Example — entering mid-pipeline:**
You already have data and a draft paper. You can enter at Strategy (skip Discovery) or even at Peer Review (skip Execution). The Orchestrator checks REQUIRES, not phase numbers.

**Example — targeted re-entry:**
A referee says "control for X." The Orchestrator routes back to coder (not through the full pipeline), coder-critic reviews, writer updates, writer-critic reviews the update, then back to peer review.

### Parallel Activation

Agents in the same PARALLEL_GROUP run concurrently when their REQUIRES are met. See `permissions.md` for the complete parallel group table.

---

## 4. Standalone Access

**Any skill can be invoked directly, bypassing the pipeline.**

### Two Modes

**Mode 1: Orchestrated (within the pipeline)**

The Orchestrator dispatches agents through the dependency graph. The user says:

> "I want to study the effect of minimum wage on employment using CPS data."

The Orchestrator activates Discovery → Strategy → Execution → Peer Review automatically.

**Mode 2: Standalone (direct access)**

The user invokes a skill directly:

> `/strategize paper/main.tex`

This runs the strategist-critic agent alone, right now, no phase dependencies.

### Why Both Modes

- **Pipeline mode** is for full projects where the Orchestrator manages the flow
- **Standalone mode** is for targeted tasks: "just check this one thing"
- Most users start with standalone skills and graduate to the pipeline

### Standalone Skills

All skills in the reference below work without pipeline context when invoked directly. They dispatch their agent(s) and return results.

| Skill | What It Does |
|-------|-------------|
| `/discover` | Literature search + data discovery |
| `/strategize` | Identification strategy design + review |
| `/analyze` | End-to-end data analysis (code + debug) |
| `/explain` | Explainer + quiz for a script — the comprehension gate |
| `/write` | Draft paper sections + humanizer pass |
| `/review` | Simulated peer review (domain + methods referees) |
| `/revise` | R&R routing per revision-protocol |
| `/talk` | Beamer talk from paper |
| `/submit` | Final gate: score >= 95, all components >= 80 |
| `/tools` | Utility skills (compile, validate-bib, commit, etc.) |

### Constraint

`/new-project` is the only skill that is always orchestrated — it exists to launch the full pipeline. Everything else can run standalone.

---

## 5. Context Management

### General Principles
- Prefer intentional `/checkpoint` + `/compact` at natural stopping points over letting auto-compression summarize for you
- Save important context to disk before it's lost
- `/clear` only when context is genuinely polluted

### Compaction Discipline

Borrowed from Goldsmith-Pinkham's Claude Code for Economists workflow:

- **Manual `/compact` before natural stopping points**, not at the threshold. You control what gets summarized.
- **Aim for 5–10 turn focused sessions.** Long sessions drift; short, scoped sessions keep output sharp.
- **Start fresh between phases.** Don't carry "discovery residue" into execution.
- **Before `/compact` or session end, run `/checkpoint`.** That persists state to memory, SESSION_REPORT, and the research journal — so the next session reads real context, not an auto-summary.

### Context Survival Strategy

**Before `/compact` or session end:**
Run `/checkpoint`. It handles:
1. Auto-memory updates (user corrections, project state, references, user profile)
2. `SESSION_REPORT.md` append per `logging.md`
3. `quality_reports/research_journal.md` append
4. (Optional) Obsidian project note if `.claude/state/obsidian-config.md` is configured

Also confirm before compaction:
- Active plan is saved to disk in `quality_reports/plans/`
- Open questions are documented

The pre-compact hook reminds you of this checklist.

**After Compression:**
First message should be: "Resuming after compression. Last task: [read most recent plan + git log + last SESSION_REPORT entry]. Status: [next step]."

### Rewind Strategy

Choose the right context management action:

- **Rewind** when Claude took a wrong approach -- removes the failed attempt from context entirely. Re-prompt with constraints upfront. Strictly superior to correction when the entire approach was wrong.
- **Correct** when the approach was right but a detail was wrong ("use state-level clustering") -- the context of the prior attempt is useful.
- **Compact** when context is bloated but the current trajectory is correct.
- **Clear** when you need a fresh start on a new task.

Rewind keeps failed exploration out of context, saving tokens and avoiding confusion on subsequent turns.

### Session Recovery

After compression or a new session, in order:
0. **Read pipeline state:** If `quality_reports/pipeline_state.json` exists, read it to determine: current phase, completed agents (with scores), in-progress agents (with round count and remaining issues), pending agents, and any blocking conditions. This is faster and more reliable than reconstructing state from prose logs.
1. **Read the most recent checkpoint artifacts:** tail of `SESSION_REPORT.md`, tail of `quality_reports/research_journal.md`, and — if `.claude/state/obsidian-config.md` exists and Obsidian MCP is connected — the latest project-note journal entry
2. Read `CLAUDE.md` + most recent plan in `quality_reports/plans/`
2. Check `git log --oneline -10` and `git diff`
3. State what you understand the current task to be
