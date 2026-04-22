---
name: ios-testflight-release
description: Release van Driver App GPS naar TestFlight via GitHub Actions. Valideert vooraf version + Apple agreement status, triggert workflow, wacht op upload, verifieert build zichtbaar in App Store Connect. Handelt bekende blockers (agreement 403, version 409) zelf af.
allowed-tools: Read, Edit, Write, Bash, mcp__claude-in-chrome__*
user-invocable: true
---

# iOS TestFlight Release — Driver App GPS

> **Doel**: Een nieuwe build van `nl.jvdp.driverappgps` in TestFlight krijgen met hard bewijs (zichtbaar in App Store Connect). Geen praatjes, alleen bewezen status.

## Aanroep

```
/skill:ios-testflight-release
```

Optioneel: `/skill:ios-testflight-release --version 2.1.2` om versie te forceren.

## Vaste feiten

- Repo: `driver_app_gps`, branch: `main`
- Bundle ID: `nl.jvdp.driverappgps`
- Team ID: `SG82Q2LN27`
- App ID in ASC: `6754825449`
- Workflow: `.github/workflows/ios-testflight.yml` (env `IOS_MARKETING_VERSION`)
- Docs (synchroniseren bij bump): `docs/appstore/RELEASE_CHECKLIST.md`, `docs/appstore/SUBMISSION_PACK.md`
- Upload via `app-store-connect publish --testflight` met ASC API key secrets (geen wachtwoord-login).

## Authenticatie

- **CI-upload**: werkt autonoom via GitHub secrets `APP_STORE_CONNECT_KEY_ID`, `APP_STORE_CONNECT_ISSUER_ID`, `APP_STORE_CONNECT_PRIVATE_KEY` + `APPLE_DIST_P12_BASE64` + `APPLE_DIST_P12_PASSWORD`.
- **UI-verificatie** (agreement + TestFlight): vereist browser-sessie op `appstoreconnect.apple.com`. 2FA blokkeert scripted login; gebruiker logt éénmalig in per sessie.
- **Nooit** Apple ID-wachtwoord in .env, scripts, of repo. Gebruik altijd de ASC API key voor machine-to-machine.

## Hard rules

1. **Geen "klaar" zonder TestFlight-screenshot** van de nieuwe build + status `Complete` of `Processing`.
2. **Geen version-bump zonder confirmation** als de eerder approved TestFlight-versie hoger is dan de target.
3. **Nooit pushen zonder expliciete "push" van gebruiker** (project-CLAUDE.md regel).
4. **Geen secrets tonen** in logs of screenshots.
5. **Fail-fast**: bij elke blocker exacte fouttekst + kleinste vervolgstap melden.

## Workflow

### Stap 1 — Pre-flight: huidige TestFlight-versie vs target

```bash
gh run list --workflow=ios-testflight.yml --limit 3 --json databaseId,conclusion,headSha,displayTitle
grep -E 'IOS_MARKETING_VERSION' .github/workflows/ios-testflight.yml
```

Vervolgens in browser: `https://appstoreconnect.apple.com/apps/6754825449/testflight/ios` → lees hoogste `VERSION & BUILD`. Dit is de floor. Target version moet **hoger zijn dan de hoogste approved build** (Apple weigert lager via 409).

### Stap 2 — Agreement status check

Navigate `https://appstoreconnect.apple.com/agreements`. Verwacht per agreement row status = `Active`. Bij:
- `Active (New Agreement Available)` → `View and Agree to Terms` knop → alleen Account Holder kan accepteren.
- Banner "The Apple Developer Program License Agreement has been updated" → klik `account` link → `Review agreement` op developer.apple.com.

Bewijs in screenshot voordat je verder gaat.

### Stap 3 — Version bump (alleen als nodig)

Als target ≤ hoogste TestFlight version: bump in 3 bestanden (één atomaire commit):
- `.github/workflows/ios-testflight.yml` — `IOS_MARKETING_VERSION: "<new>"`
- `docs/appstore/RELEASE_CHECKLIST.md` — `- Marketing version in Xcode-project: \`<new>\``
- `docs/appstore/SUBMISSION_PACK.md` — `- Marketing version: \`<new>\``

Commit: `chore(ios): bump marketing version to <new>` met reden in body.

**Stop hier** voor expliciete push-GO van gebruiker. Nooit stilletjes naar main pushen.

### Stap 4 — Trigger + watch

```bash
gh workflow run ios-testflight.yml --ref main
RUN_ID=$(gh run list --workflow=ios-testflight.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch $RUN_ID --exit-status
```

Loop de stappen door tot `Upload to TestFlight` groen is.

### Stap 5 — Bekende blockers automatisch herkennen

| Fouttekst in log | Root cause | Fix |
|---|---|---|
| `403: A required agreement is missing or has expired` in `Fetch Provisioning Profiles` | Apple Developer/Paid Apps Agreement update onbehandeld | Terug naar stap 2; Account Holder accepteert agreement |
| `409 ... must contain a higher version than previously approved version [X]` in `Upload to TestFlight` | Semver-conflict met eerder approved build | Terug naar stap 3; bump boven X |
| `No certificate for team 'SG82Q2LN27' matching` | Distribution p12 secret missing/expired | Rotate `APPLE_DIST_P12_BASE64` in repo secrets |
| `401 Unauthorized` op ASC | API key ingetrokken | Rotate ASC key trio in repo secrets |

### Stap 6 — TestFlight-verificatie (hard bewijs)

Refresh `https://appstoreconnect.apple.com/apps/6754825449/testflight/ios`. Verwacht:
- `Build Uploads`-rij met nieuwe version + status `Processing` of `Complete`
- `Version <new>` sectie met build-nummer + status (`Waiting for Review` is normaal voor external testers; internal testers krijgen direct toegang).

Screenshot = bewijs.

## Eindrapport (verplicht)

Rapporteer exact één van:

- `TRIGGERED` — workflow gestart, nog niet klaar
- `BUILDING` — in_progress
- `UPLOAD_FAILED <exacte fouttekst + step>`
- `TESTFLIGHT_PROCESSING` — build geupload, Apple verwerkt nog
- `TESTFLIGHT_READY` — build `Complete`, zichtbaar + approved voor testers
- `BLOCKED <exacte fouttekst + kleinste vervolgstap>`

Plus:
- Run URL: `https://github.com/jongensutrecht/driver_app_gps/actions/runs/<id>`
- Commit SHA (bij bump)
- Screenshot-ID van TestFlight-pagina

## Niet doen

- Geen `--no-verify` op commits
- Geen force-push naar main
- Geen Apple ID-wachtwoord invullen in browser
- Geen mock-status rapporteren zonder screenshot
- Geen `1.x` versie proberen als `2.x` al approved is (Apple weigert)
