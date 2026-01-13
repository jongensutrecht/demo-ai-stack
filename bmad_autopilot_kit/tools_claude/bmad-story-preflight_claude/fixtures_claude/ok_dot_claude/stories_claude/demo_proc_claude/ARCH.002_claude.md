# Story ARCH.002: Fixture - dot IDs + multiple ACs

## Context
- Fixture repo voor preflight: meerdere ACs met canonieke markers.

## Story
Als **tester** wil ik **meerdere ACs** zodat **per-AC enforcement** getest wordt.

## Acceptance Criteria
- **AC1:** Repo-root verification werkt.
  - **Verification (repo-root):** `pwsh -NoProfile -Command "exit 0"`
  - **Expected:** `exit code 0`
- **AC2:** CWD verification werkt.
  - **Verification (cwd=docs):** `pwsh -NoProfile -Command "exit 0"`
  - **Expected:** `exit code 0`

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

