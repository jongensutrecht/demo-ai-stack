# Demo AI Stack

> BMAD Autopilot + CTO Guard + Ralph Loop voor Claude Code

Een complete, deelbare workflow voor story-driven development met kwaliteitsgaranties.

---

## Wat zit erin?

| Component | Functie |
|-----------|---------|
| `skills/` | Skill-pack (bmad-autopilot, bmad-bundle, plan-to-bmad, ralph-loop, cto-guard, test-guard, invariant-discovery, quick-fix, skill-creator) |
| `bmad_autopilot_kit/` | Prompts, preflight scripts, templates |
| `docs/CTO_RULES.md` | CTO review criteria (11 facetten) |

---

## Installatie

### Optie A: PowerShell (Windows)

```powershell
.\INSTALL.ps1
```

### Optie B: Handmatig

1. **Kopieer skills naar global:**
   ```powershell
   Copy-Item -Recurse .\skills\* $env:USERPROFILE\.claude\skills\
   ```

2. **Kopieer kit naar je project:**
   ```powershell
   Copy-Item -Recurse .\bmad_autopilot_kit\ <jouw-project>\bmad_autopilot_kit\
   Copy-Item .\docs\CTO_RULES.md <jouw-project>\docs\
   ```

---

## Gebruik

### 1. Start BMAD Autopilot

```
/bmad-autopilot
```

Vraagt om input .md bestand, genereert stories met CTO traceability.

### 2. CTO Guard (standalone)

```
/cto-guard
```

Valideert code of stories tegen `docs/CTO_RULES.md`.

### 3. Ralph Loop (automatische iteratie)

```
/ralph-loop
```

Itereert over BACKLOG.md tot alle stories [DONE] of [BLOCKED].

---

## Workflow Diagram

```
Input .md document
       │
       ▼
┌──────────────────┐
│ CTO GUARD #1     │  PRE-GENERATION
│ Valideer input   │
└──────────────────┘
       │ ✅
       ▼
┌──────────────────┐
│ RUN1: Stories    │  Genereer OPS-001, OPS-002, ...
│ + BACKLOG.md     │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ CTO GUARD #2     │  POST-GENERATION
│ Valideer stories │
└──────────────────┘
       │ ✅
       ▼
┌──────────────────┐
│ RALPH LOOP       │  Per story:
│                  │  - Voer uit
│                  │  - Gate A (ruff + pytest)
│                  │  - CTO Guard #3
│                  │  - Update BACKLOG
└──────────────────┘
       │
       ▼
   Alle [DONE]
```

---

## Vereisten

- Claude Code CLI
- PowerShell (Windows) of Bash (Mac/Linux)
- Git
- Python + ruff + pytest (voor Gate A)

---

## Folder Structuur na Installatie

```
~/.claude/
└── skills/
    ├── bmad-autopilot/
    ├── bmad-bundle/
    ├── plan-to-bmad/
    ├── ralph-loop/
    ├── cto-guard/
    ├── test-guard/
    ├── invariant-discovery/
    ├── quick-fix/
    └── skill-creator/

<jouw-project>/
├── bmad_autopilot_kit/
│   ├── RUN1_STORY_GENERATION_PROMPT.txt
│   └── tools/
├── docs/
│   ├── CTO_RULES.md
│   └── CONTRACT.md
└── stories/<process>/
    ├── OPS-001.md
    ├── OPS-002.md
    └── BACKLOG.md
```

---

## CTO Guard Output (5 secties)

1. **CTO RULES APPLIED** - Welke regels gebruikt
2. **TRACEABILITY MAP** - Waar elke regel gedekt is
3. **VIOLATIONS** - Hard/soft violations
4. **REQUIRED ACTIONS** - Wat moet fixen
5. **VERDICT** - ✅ COMPLIANT / ⚠️ CONDITIONAL / ❌ NON-COMPLIANT

---

## Verdicts

| Verdict | Betekenis | Actie |
|---------|-----------|-------|
| ✅ COMPLIANT | Alles voldoet | Doorgaan |
| ⚠️ CONDITIONAL | Soft violations | Doorgaan, fix binnen sprint |
| ❌ NON-COMPLIANT | Hard violations | BLOKKEER tot gefixed |

---

## Versie

- **Demo AI Stack**: 1.0.0
- **Datum**: 2026-01-13
- **Auteur**: Mr. Biggles + Claude

---

## Licentie

MIT - Vrij te gebruiken en aan te passen.
