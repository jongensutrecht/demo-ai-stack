# Photobooth PC Cleanup Scripts

Agressieve Windows 11 bloatware removal voor een dedicated photobooth PC.

## Vereisten

- Windows 11
- PowerShell als Administrator
- Google Chrome geïnstalleerd
- Darkroom Booth geïnstalleerd
- Printer spooler software geïnstalleerd

## Gebruik

**Maak eerst een herstelpunt!**

```powershell
# Stap 0: Herstelpunt maken
Checkpoint-Computer -Description "Pre-cleanup"

# Stap 1: Bloatware verwijderen
powershell -ExecutionPolicy Bypass -File cleanup-photobooth-pc.ps1

# Stap 2: Chrome afslanken
powershell -ExecutionPolicy Bypass -File chrome-lockdown.ps1

# Stap 3: Herstart
Restart-Computer
```

## Wat wordt behouden

| Component | Status |
|---|---|
| Windows Core (kernel, shell, networking) | Behouden |
| Print Spooler | Behouden + Automatic |
| Darkroom Booth | Onaangetast |
| Google Chrome | Behouden, gestript tot kale browser |
| Windows Store | Behouden (systeem-updates) |
| Windows Update | Behouden |

## Wat wordt verwijderd/uitgeschakeld

- Alle pre-installed apps (Xbox, Mail, Kaarten, Weer, Nieuws, Teams, Copilot, etc.)
- OneDrive (volledig)
- Edge (geneutraliseerd, achtergrond uit)
- 30+ onnodige services (telemetrie, Xbox, telefonie, biometrie, etc.)
- Telemetrie en diagnostiek
- Notificaties, tips, suggesties, reclame
- Windows Recall, Cortana, Widgets, Chat
- Chrome: sync, AI, extensies, autofill, wachtwoorden, notificaties, camera/mic
