# BACKLOG.md Format

## Template

```markdown
# BACKLOG - [Process Name]

> Gegenereerd door BMAD Autopilot
> Laatst bijgewerkt: YYYY-MM-DD HH:MM

---

## Status Legend

| Status | Meaning |
|--------|---------|
| [TODO] | Not started |
| [IN_PROGRESS] | Currently being worked on |
| [DONE] | Completed successfully |
| [BLOCKED] | Failed after max attempts |

---

## Stories

| Story | Title | Status | Attempts | Test Gate | Invariant Check | Notes |
|-------|-------|--------|----------|-----------|-----------------|-------|
| OPS-001 | Setup project structure | [DONE] | 1 | ✅ | ✅ | |
| OPS-002 | Implement user auth | [IN_PROGRESS] | 1 | ⏳ | ⏳ | Working on NEVER-tests |
| OPS-003 | Add dashboard UI | [TODO] | 0 | - | - | |
| OPS-004 | API endpoints | [TODO] | 0 | - | - | |
| OPS-005 | Integration tests | [BLOCKED] | 3 | ❌ | ✅ | Missing playwright |

---

## Progress

- Total Stories: 5
- Completed: 1 (20%)
- In Progress: 1
- Blocked: 1
- Remaining: 2

---

## Blocked Stories

### OPS-005: Integration tests

**Reason**: Missing playwright tests after 3 attempts

**Last Error**:
```
test-gate.ps1 exit 1:
- Missing playwright test for components/DataGrid.tsx
- Missing playwright test for pages/Dashboard.tsx
```

**Resolution Required**:
1. Create `tests/e2e/data-grid.spec.ts`
2. Create `tests/e2e/dashboard.spec.ts`
3. Manually re-run story

---

## Changelog

| Timestamp | Story | Action | Result |
|-----------|-------|--------|--------|
| 2026-01-17 10:00 | OPS-001 | Started | IN_PROGRESS |
| 2026-01-17 10:15 | OPS-001 | Gate A passed | DONE |
| 2026-01-17 10:20 | OPS-002 | Started | IN_PROGRESS |
| 2026-01-17 10:45 | OPS-005 | Attempt 3 failed | BLOCKED |
```

---

## Field Descriptions

### Story
Story ID matching the filename (e.g., `OPS-001` for `OPS-001.md`)

### Title
Short description of what the story does

### Status
One of: `[TODO]`, `[IN_PROGRESS]`, `[DONE]`, `[BLOCKED]`

### Attempts
Number of times this story has been attempted (max 3)

### Test Gate
Result of `test-gate.ps1`:
- `✅` - All required tests present
- `❌` - Missing required tests
- `⏳` - Not yet checked
- `-` - Not started

### Invariant Check
Result of `invariant-check.ps1`:
- `✅` - All invariants have NEVER-tests
- `❌` - Missing NEVER-tests
- `⏳` - Not yet checked
- `-` - Not started

### Notes
Any relevant notes or error messages

---

## Status Transitions

```
[TODO] ──start──> [IN_PROGRESS]
           │
           ├──success──> [DONE]
           │
           └──fail (3x)──> [BLOCKED]

[BLOCKED] ──manual fix + retry──> [IN_PROGRESS]
```

---

## Updating the BACKLOG

### On Story Start
```markdown
| OPS-002 | Implement user auth | [IN_PROGRESS] | 1 | ⏳ | ⏳ | Started |
```

### On Story Success
```markdown
| OPS-002 | Implement user auth | [DONE] | 1 | ✅ | ✅ | |
```

### On Story Failure
```markdown
| OPS-002 | Implement user auth | [IN_PROGRESS] | 2 | ❌ | ✅ | Retry 2: missing unit test |
```

### On Story Blocked
```markdown
| OPS-002 | Implement user auth | [BLOCKED] | 3 | ❌ | ✅ | Missing playwright after 3 attempts |
```
