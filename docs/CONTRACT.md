# BMAD Story Contract

> Dit contract definieert het verplichte format voor BMAD stories.

---

## Story File Format

Elke story (`OPS-XXX.md`) MOET deze secties bevatten in deze volgorde:

### Verplichte Headers
1. Context
2. Story
3. Acceptance Criteria (met CTO traceability)
4. Tasks/Subtasks
5. Dev Notes
6. Dev Agent Record
7. Status

---

## Hard Rules

1. **Eerste taak**: Altijd `Lees CLAUDE.md`
2. **Laatste taak**: Altijd `Run Gate A checks`
3. **CTO Traceability**: Elke AC heeft CTO Rule + Facet
4. **Verification**: Elke AC heeft executable command + expected output
5. **Touched Paths**: Expliciete allowlist van bestanden

---

## AC Format (per Acceptance Criterium)

```
### AC1: [Naam]
- **Given**: [Precondities]
- **When**: [Actie]
- **Then**: [Resultaat]
- **CTO Rule**: `[RULE-ID]`
- **CTO Facet**: `[Facet naam]`
- **Verification (repo-root)**: `[command]`
- **Expected**: `[output/exit]`
```

---

## BACKLOG.md Format

```markdown
# BACKLOG - [Process]

| Story | Status | Attempts | Notes |
|-------|--------|----------|-------|
| OPS-001 | [TODO] | 0 | |
| OPS-002 | [TODO] | 0 | |
```

Statussen: [TODO], [IN_PROGRESS], [DONE], [BLOCKED]

---

CONTRACT v1.0.0 - 2026-01-13
