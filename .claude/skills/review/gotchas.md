# Review Skill -- Gotchas

Known failure points and edge cases for paper/code/strategy review.

- Editor's desk review may desk-reject incomplete drafts -- specify submission stage explicitly if the paper is early-stage.
- Early-stopping in causal audit: Phase 2 critical issues override Phases 3-4 checks. This is by design -- fatal identification flaws make downstream checks moot.
- Peer review dispositions are assigned by the editor, not random -- user can influence by specifying journal culture in the request.
- Advisory scoring for talks means low scores don't block pipeline progression.
- Cold-read protocol means critics don't see prior rounds -- they may flag the same issue differently across rounds. This is a feature, not a bug.
- Code review checks both the script AND its output. A script that runs clean but produces wrong numbers still fails.
- Writer-critic deductions from `thesis-format.md` are required (blocking), not advisory. Missing `\doublespacing` is -5, not a suggestion.
- Voice fidelity (writer-critic category 7) is only scored when `.claude/references/personal-style-guide.md` has real content. If the style guide is still a template, skip and report.
- The strategist-critic uses severity classification (CRITICAL/MAJOR/MINOR), not a point-deduction rubric. The coder-critic and writer-critic use point deductions.
- Theorist-critic should not lecture authors on their own methods. Check `.claude/references/domain-profile.md` for the paper's authors before flagging textbook issues.
- Explorer-critic flags concerns but does NOT suggest specific alternative datasets (separation of powers).
- R&R second round reloads same referee dispositions and pet peeves from round 1. Max 3 rounds total.
- The editor is NOT a third referee -- they synthesize and decide, not add new substantive criticisms.
- When reviewing structural papers, don't penalize for missing parallel trends. When reviewing descriptive papers, don't penalize for missing identification. Paper-type awareness is mandatory for all critics.
- The data-review template says "4 categories" in the task spec but the explorer-critic actually checks 6 dimensions. The template file uses the full 6.
