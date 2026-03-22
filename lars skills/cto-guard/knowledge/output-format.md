# CTO Guard Output Format (Universal CTO Review v2.5)

`/skill:cto-guard` is the executable entrypoint for the **full** Universal CTO Review v2.5.
It is **not** allowed to collapse the review to a short verdict-only summary.
The review is only complete when the **full repo-10x contract (A-I)** is also assessed inside the same report.

## Mandatory report shape

Return **one markdown report** with exactly these top-level sections:

1. **Executive Summary**
2. **Facet Scores Overview**
3. **Per-facet detail**
4. **Consolidated Gap Table**
5. **Prioritized Action Plan**
6. **Path to 10/10**

Also mandatory around that report:
- execute the full scan contract from `docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md`
- write the report to `docs/CTO_REVIEW_<repo>.md`
- if unresolved gaps remain and the user did not say `review-only`: generate BMAD follow-up input in a unique `main-merge` worktree
- after the full report, add a short **Jip-en-Janneke TL;DR** in chat with:
  - overall status
  - overall score
  - the score per facet
  - whether BMAD follow-up was triggered

## 1) Executive Summary

Must contain, explicitly:
- `Repo: <absolute repo path>`
- review target (`repo`, `working tree`, `diff`, `story`, `plan`, or `mixed`)
- review scope (`repo_only`, `repo_plus_db`, `repo_plus_infra`, `full_stack`, or justified limited delta scope)
- repo archetype(s)
- audit target (`HEAD` or `working tree`)
- `in scope`
- `out of scope`
- `UNKNOWN external state`
- repo / branch / commit / clean-or-dirty if available
- overall status (`PASS` / `FAIL`)
- final verdict (`COMPLIANT` / `CONDITIONAL` / `NON-COMPLIANT`)
- overall score if scorable
- confidence (`HIGH` / `MEDIUM` / `LOW`)
- short bottom line in plain language
- **Repo-10x contract snapshot** with explicit status for A-I (`PASS` / `FAIL` / `UNKNOWN`) and 1-line evidence each

Fail-closed rule:
- if repo/branch/commit/scope cannot be proven, mark the unknown explicitly and give exactly 1 concrete verification check.

## 2) Facet Scores Overview

Use the Universal CTO v2.5 facet model.
For **each** facet, report:
- applicability: `Applicable` / `N/A` / `UNKNOWN`
- score or `N/A` / `UNKNOWN`
- confidence
- owned unresolved gaps
- short note

Mandatory facets:
1. Architectuur
2. Code Quality
3. Complexity & Bugs
4. Testing
5. Dependencies
6. Security
7. Ops/Reliability
8. Documentation
9. Developer Experience
10. Feature Flags
11. Domain/Spec Compliance

Do **not** omit P3-class concerns from scoring notes.
If a facet is `N/A`, give exactly 1 evidence line.
If a facet is `UNKNOWN`, give exactly 1 verification check.

## 3) Per-facet detail

For every `Applicable` facet, include a dedicated subsection with:
- applicability
- score
- confidence
- 1-3 strengths with evidence
- **CTO Rules Applied**
- **Traceability Map** (rule/facet/guardrail -> covered? -> evidence)
- unresolved gaps table

Gap table columns:
- `ID`
- `Primary Owner`
- `Priority`
- `Status`
- `Gap`
- `Evidence`
- `Closure DoD`
- `Cross-refs`

Priority values:
- `P1-CRITICAL`
- `P1-QUICK`
- `P2`
- `P3`

Status values:
- `OPEN`
- `PARTIAL`
- `DONE`

Hard rule:
- `P3` items must be shown explicitly when present; never silently drop them.

## 4) Consolidated Gap Table

Provide **one canonical combined table** for all gaps.
Each root cause may appear only once as the canonical row.
Repo-10x A-I failures must be mapped into this same canonical table; do not keep them in a separate disconnected checklist.

Columns:
- `ID`
- `Primary Owner`
- `Priority`
- `Status`
- `Summary`
- `Evidence`
- `Closure DoD`
- `Cross-refs`

Rules:
- only unresolved gaps (`OPEN`, `PARTIAL`) count against the score
- `DONE` may be shown for context but does not penalize scoring
- the same root cause must not be double-counted across facets

## 5) Prioritized Action Plan

Group actions by:
- `P1-CRITICAL`
- `P1-QUICK`
- `P2`
- `P3`

For each action include:
- action title
- exact files/areas affected
- why it matters
- evidence link
- concrete closure condition

Never omit the `P3` section.
If there are no actions in a group, write `None` explicitly.

## 6) Path to 10/10

Must include:
- what blocks `10/10` right now
- what is already strong
- which unknowns still block a hard 10/10 claim
- exact order of attack to reach green
- whether the current change may proceed or must be blocked
- **Repo-10x closure summary**: which of A-I are already `PASS`, which are not, and what exactly still blocks a hard green repo verdict

## Verdict model

Allowed final verdicts:
- `COMPLIANT`
- `CONDITIONAL`
- `NON-COMPLIANT`

Also report Universal CTO status:
- overall status (`PASS` / `FAIL`)
- overall score (if scorable)
- confidence

Interpretation:
- `COMPLIANT` = no blocking violations in reviewed scope **and** no unresolved repo-10x blockers remain
- `CONDITIONAL` = functionally acceptable but unresolved non-blocking gaps remain
- `NON-COMPLIANT` = unresolved blocking gap(s); stop until fixed

Hard rule:
- A review may not claim a hard all-green / fully-good result if any repo-10x contract item A-I is still `FAIL` or blocking `UNKNOWN`.

## Evidence rules

Every claim must have one of:
- `path:line`
- command + relevant output
- explicit `UNKNOWN` + exactly 1 verification check

Never claim:
- "looks good"
- "probably fine"
- implicit compliance without evidence

## Minimum richness rule

A valid CTO Guard report is invalid if it only contains:
- a short verdict block
- only rule mapping
- only P1/P2 without facet scoring
- no explicit `P3`
- no `Facet Scores Overview`
- no `Path to 10/10`

If the report is shorter than the information needed to score the applicable facets, it is incomplete.

## Post-review BMAD hook (operational rule)

Do **not** add a 7th mandatory top-level section.
If the BMAD hook runs, report it inside **Path to 10/10** with:
- `triggered: yes`
- generated file paths
- worktree path
- mapping summary from review priorities to BMAD priorities
- whether the BMAD input was committed

Default mapping:
- `P1-CRITICAL` / `P1-QUICK` -> BMAD `P0`
- `P2` -> BMAD `P1`
- `P3` -> BMAD `P3`

If there are no unresolved gaps, or the user explicitly asked `review-only`, report:
- `triggered: no`

## Chat TL;DR (operational rule)

After the full markdown report, provide a short Jip-en-Janneke TL;DR in chat.
Mandatory content:
- one line: `Eindoordeel: <verdict> | Score: <overall>`
- one bullet per facet with the score or `N/A` / `UNKNOWN`
- one bullet: grootste probleem in simpele taal
- one bullet: BMAD follow-up wel/niet gemaakt
