# BMAD story preflight (RUN1 output check)

Doel: voor je RUN2 (runner build) uitvoert, valideren dat RUN1 correcte story files heeft gemaakt:
- story IDs en bestandsnamen zijn contractueel (hyphen + dot)
- per AC: exact 1 `Verification` + 1 `Expected` (fail-closed)
- touched paths allowlist bestaat en is niet leeg
- (optioneel) `PROCESS.md` canonical order matcht met story files

Bij errors: exit code `2` (fail-closed), tenzij je `-WarnOnly` gebruikt.

## Wat wordt gecheckt
- Stories in `stories/<process>/` met bestandsnaam `PREFIX-001.md` of `PREFIX.001.md`
- `## Acceptance Criteria`: elke `**ACn:**` heeft exact 1 verification-pair
  - Canoniek: `- **Verification (repo-root):** \`...\`` en `- **Expected:** \`...\``
  - Legacy compat: `- Verification ...` en `- Expected: ...`
- `### Touched paths allowlist`: minimaal 1 repo-relatief pad
- `## Status`: `ready-for-dev` (of `drafted` alleen met `-AllowDrafted`)

## Gebruik

```powershell
pwsh ./bmad_autopilot_kit/tools/bmad-story-preflight/preflight.ps1 `
  -RepoRoot "C:\path\to\repo-root"
```

Als je meerdere processen hebt:

```powershell
pwsh ./bmad_autopilot_kit/tools/bmad-story-preflight/preflight.ps1 `
  -RepoRoot "C:\path\to\repo-root" `
  -Process "mijn_process"
```

Als je drafted stories tijdelijk wil toestaan (alleen warnings):

```powershell
pwsh ./bmad_autopilot_kit/tools/bmad-story-preflight/preflight.ps1 `
  -RepoRoot "C:\path\to\repo-root" `
  -AllowDrafted
```

Als je machine-readable output wil (voor tooling/CI):

```powershell
pwsh ./bmad_autopilot_kit/tools/bmad-story-preflight/preflight.ps1 `
  -RepoRoot "C:\path\to\repo-root" `
  -Process "mijn_process" `
  -JsonOutput ".\\artifacts\\preflight.json"
```

Self-check (fixtures, end-to-end):

```powershell
pwsh ./bmad_autopilot_kit/tools/bmad-story-preflight/self_check.ps1
```
