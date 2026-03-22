---
name: fixed-port-discipline
description: Enforces fixed-port behavior for any repo. Use when starting local dev, test, preview, API, or tunnel processes. Always use the port declared in repo config/scripts/docs; if occupied, inspect and kill the conflicting local listener, then start on that same port instead of port hopping.
allowed-tools: read bash edit write
---

# Fixed Port Discipline

Gebruik deze skill zodra een taak lokale services start of herstart.

## Kernregel

**Geen port hopping.**

Universele guards: zie `~/.pi/agent/skills/_guards.md`.

Als een repo/config/script/docs een port aanwijst, dan is dat de canonieke port voor die flow.

- Gebruik exact die port.
- Is die port bezet, inspecteer het proces.
- Kill het conflicterende lokale proces.
- Start de nieuwe instance daarna op **dezelfde** port.
- Wijk alleen af naar een andere port als de gebruiker dat expliciet vraagt.

## Verplicht protocol

1. Lees eerst de repo-config, scripts of docs om de canonieke port vast te stellen.
2. Check de listener op die port.
3. Inspecteer PID + commandline.
4. Maak de port vrij.
5. Start de gewenste service op dezelfde port.
6. Verifieer dat de nieuwe service nu op die port luistert.

## Helper script

Gebruik deze helper vanuit deze skill:

```bash
./scripts/ensure-port.sh <port> <label>
```

Voorbeeld:

```bash
cd /home/mrbiggles/.pi/agent/skills/fixed-port-discipline
./scripts/ensure-port.sh 4010 local-dev-server
```

## Veiligheidsregel

Deze skill is bedoeld voor conflicterende **lokale dev/test/preview-processen** binnen gebruikersrechten.

Als de listener geen vervangbaar lokaal proces is of buiten gebruikersrechten valt, rapporteer dan exact:
- welke port bezet is
- welk proces erop luistert
- welke check faalde

## Verboden

- spontaan uitwijken naar een andere port
- de gebruiker vragen zelf een proces te killen
- een repo-config negeren omdat een alternatieve port "nu even makkelijker" is
- succes claimen zonder te verifiëren dat de nieuwe service echt op de canonieke port luistert
