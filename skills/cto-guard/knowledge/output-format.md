# CTO Guard Output Format (Universal CTO Review v2.4)

`/cto-guard` is the executable entrypoint for the **full** Universal CTO Review v2.4.
It is **not** allowed to collapse the review to a short verdict-only summary.

## Mandatory report shape

Return **one markdown report** with exactly these top-level sections:

1. **Executive Summary**
2. **Facet Scores Overview**
3. **Per-facet detail**
4. **Consolidated Gap Table**
5. **Prioritized Action Plan**
6. **Path to 10/10**

## 1) Executive Summary

Must contain, explicitly:
- review target (`repo`, `working tree`, `diff`, `story`, `plan`, or `mixed`)
- review scope (`repo_only`, `repo_plus_db`, `repo_plus_infra`, `full_stack`, or justified limited delta scope)
- `in scope`
- `out of scope`
- `UNKNOWN external state`
- `source documents consulted`
- repo / branch / commit / clean-or-dirty if available
- overall status (`PASS` / `FAIL` / `CONDITIONAL` / `NON-COMPLIANT`)
- overall score if scorable
- confidence (`HIGH` / `MEDIUM` / `LOW`)
- short bottom line in plain language
- if historical audit/gap docs were used: whether each carried finding was revalidated or marked `historical-only`

Fail-closed rule:
- if repo/branch/commit/scope cannot be proven, mark the unknown explicitly and give exactly 1 concrete verification check.

## 2) Facet Scores Overview

Use the Universal CTO v2.4 facet model.
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
- `COMPLIANT` = no blocking violations in reviewed scope
- `CONDITIONAL` = functionally acceptable but unresolved non-blocking gaps remain
- `NON-COMPLIANT` = unresolved blocking gap(s); stop until fixed

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

If `docs/CTO_GUARD_PROJECT_ADDENDUM.md` exists, the report is also incomplete when it omits the addendum's mandatory repo-specific checks.

## Post-review BMAD hook (operational rule)

Do **not** add a 7th mandatory top-level section.
If the BMAD hook runs, report it inside **Path to 10/10** with:
- `triggered: yes`
- generated file paths
- mapping summary from review priorities to BMAD priorities

Default mapping:
- `P1-CRITICAL` / `P1-QUICK` -> BMAD `P0`
- `P2` -> BMAD `P1`
- `P3` -> BMAD `P3`

If there are no unresolved gaps, or the user explicitly asked `review-only`, report:
- `triggered: no`
