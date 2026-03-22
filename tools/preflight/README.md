# BMAD story preflight (RUN1 output check)

Doel: vóór RUN2 valideren dat RUN1 correcte story files heeft gemaakt.

Bij errors: exit code `2` (fail-closed), tenzij je `-WarnOnly` gebruikt.

## Wat wordt gecheckt
- stories in `stories/<process>/` met contractuele bestandsnamen
- per AC exact 1 `Verification` + 1 `Expected`
- touched paths allowlist bestaat en is niet leeg
- optioneel: `PROCESS.md` canonical order matcht met story files

## Gebruik in deze repo

```powershell
pwsh ./tools/preflight/preflight.ps1 -RepoRoot .
```

Met expliciet proces:

```powershell
pwsh ./tools/preflight/preflight.ps1 -RepoRoot . -Process "mijn_process"
```

Met JSON output:

```powershell
pwsh ./tools/preflight/preflight.ps1 -RepoRoot . -Process "mijn_process" -JsonOutput ".\artifacts\preflight.json"
```

## Gebruik in geëxporteerde kit

De huidige export staat onder:
- `bmad_autopilot_kit/tools_claude/bmad-story-preflight_claude/preflight_claude.ps1`

Gebruik daarvoor het geëxporteerde pad letterlijk; de oude verwijzing naar `bmad_autopilot_kit/tools/bmad-story-preflight/` is niet canoniek in deze repo.
