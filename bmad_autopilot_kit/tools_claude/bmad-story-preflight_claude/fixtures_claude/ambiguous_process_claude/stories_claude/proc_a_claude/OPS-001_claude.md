# Story OPS-001: Fixture - ambiguous process

## Context
- Dummy file; deze fixture moet falen vóór parsing (process auto-detect is ambigue).

## Story
Als **tester** wil ik **ambigue procesdetectie** zodat **preflight fail-closed stopt**.

## Acceptance Criteria
- **AC1:** Onbereikbaar in deze fixture.
  - Verification (repo-root): `pwsh -NoProfile -Command "exit 0"`
  - Expected: `exit code 0`

## Tasks / Subtasks
- [ ] N.v.t.

## Dev Notes
### Touched paths allowlist (repo-relatief, exact)
- `README.md`

## Dev Agent Record
### Completion Notes List
- TBD

### File List
- TBD

## Status
ready-for-dev

