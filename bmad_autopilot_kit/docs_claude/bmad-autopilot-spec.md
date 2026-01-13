# BMAD Autopilot Specification

**Status:** Active
**Owner:** Alexander
**Last Updated:** 2026-01-07

## Overview

De BMAD (Build-Measure-Adjust-Deliver) Autopilot is een geautomatiseerd systeem voor het uitvoeren van story-driven development via AI agents (Claude Code / Codex).

## Architecture

```
bmad_autopilot_kit_claude/          # Kit voor Claude Code
├── UITVOER_PROMPT_claude.md        # Hoofdprompt (entry point)
├── RUN1_STORY_GENERATION_PROMPT_claude.txt
├── RUN2_RUNNER_IMPLEMENTATION_PROMPT_AUTOEXEC_claude.txt
└── tools_claude/                   # Preflight tooling

tools/story-runner/                 # SINGLE SOURCE OF TRUTH
├── run_stories.ps1                 # Hoofdrunner (ondersteunt -ClaudeCommand EN -CodexCommand)
├── run_autopilot_detached.ps1      # Detached launcher
├── lib/                            # Shared libraries
│   ├── git_worktrees.ps1
│   ├── run_commands.ps1
│   ├── run_state.ps1
│   └── ...
└── runs/                           # Run output per process
```

## CRITICAL: Single Source of Truth

### Story Runner

| Aspect | Waarde |
|--------|--------|
| **Locatie** | `tools/story-runner/` |
| **Ondersteunt** | `-ClaudeCommand` EN `-CodexCommand` |
| **NOOIT** | Nieuwe versie genereren in `tools_claude/` of elders |

De story-runner ondersteunt BEIDE CLI's via parameters. Er is geen aparte Claude of Codex versie nodig.

### Anti-Pattern: Nieuwe Versies Genereren

```
❌ FOUT:
   AI krijgt taak: "Maak story-runner voor Claude"
   AI maakt: nieuwe versimpelde versie in tools_claude/story-runner/
   Resultaat: Broken code, missing features, duplicatie

✅ CORRECT:
   AI krijgt taak: "Maak story-runner voor Claude"
   AI checkt: tools/story-runner/ bestaat al
   AI checkt: ondersteunt al -ClaudeCommand (commit 69ad9f5)
   AI doet: NIETS - het werkt al
```

## Rules for AI Agents

### Rule 1: Check Before Generate

Voordat je IETS genereert, check:
1. Bestaat er al een werkende versie?
2. Ondersteunt die versie al wat gevraagd wordt?
3. Zo ja: STOP. Gebruik de bestaande versie.

### Rule 2: Extend, Don't Replace

Als je functionaliteit moet toevoegen:
1. KOPIEER NIET de hele file
2. MAAK GEEN nieuwe versimpelde versie
3. VOEG TOE aan de bestaande code
4. BEHOUD alle bestaande features

### Rule 3: Git History is Documentation

Bekijk git history voordat je wijzigt:
```bash
git log --oneline -10 -- <path>
```

Als er recente commits zijn met "fix", "feat", "compatibility" - de code is actief onderhouden.

### Rule 4: No tools_claude/ Duplicatie

De `tools_claude/` folder is ALLEEN voor:
- Preflight scripts specifiek voor BMAD kit
- NOOIT voor duplicatie van `tools/`

Als je merkt dat je code kopieert van `tools/` naar `tools_claude/`: STOP. Dat is het anti-pattern.

## Story Runner Parameters

```powershell
# Voor Codex
.\tools\story-runner\run_stories.ps1 `
  -Process "my_process" `
  -CodexCommand 'codex exec ...'

# Voor Claude
.\tools\story-runner\run_stories.ps1 `
  -Process "my_process" `
  -ClaudeCommand 'claude.cmd --dangerously-skip-permissions -p ...'
```

Beide gebruiken DEZELFDE runner. Geen aparte versies.

## Features (die NIET verloren mogen gaan)

| Feature | Beschrijving | VERPLICHT |
|---------|--------------|-----------|
| Timeouts | 2400s default per story | ✅ |
| Retry logic | -MaxAttemptsPerStory | ✅ |
| Run state | lib/run_state.ps1 | ✅ |
| Skip merged | -SkipAlreadyMerged | ✅ |
| Gate checks | Pre/post integration gates | ✅ |
| Worktree management | lib/git_worktrees.ps1 | ✅ |
| Command execution | lib/run_commands.ps1 | ✅ |
| Detached mode | run_autopilot_detached.ps1 | ✅ |

## Incident Log

### 2026-01-06: Duplicate Runner Generation

**Wat gebeurde:**
- BMAD autopilot genereerde `tools_claude/story-runner/`
- Nieuwe versie miste: timeouts, retry logic, run state, skip merged
- 37% minder code dan werkende versie

**Root cause:**
- AI las niet eerst wat er al bestond
- AI genereerde nieuwe versie i.p.v. bestaande te gebruiken

**Oplossing:**
- `tools_claude/story-runner/` verwijderd
- Deze spec aangemaakt
- Rule: Check Before Generate

## Verification

Bij elke BMAD run, check:
```powershell
# Mag NIET bestaan
Test-Path "tools_claude/story-runner/" # Should be False

# MOET bestaan
Test-Path "tools/story-runner/run_stories.ps1" # Should be True
```

## References

- `tools/story-runner/README.md`
- `bmad_autopilot_kit_claude/RUNBOOK_BMAD_RUN1_RUN2_SOP_claude.md`
- Git commits: 1d81404, e6ba738, 69ad9f5, 17767a4
