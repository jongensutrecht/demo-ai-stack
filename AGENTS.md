# Agent Instructions (demo-ai-stack)

## Default mode: zelfstandig doorwerken
- Werk taken end-to-end af zonder om gebruikersinput te vragen.
- Ga na elke afgeronde stap direct door met de volgende beste stap.
- Vraag alleen iets aan de gebruiker als:
  1. een actie destructief of irreversibel is;
  2. er meerdere realistische keuzes zijn met duidelijk verschillende uitkomsten;
  3. essentiële informatie ontbreekt die niet uit code, docs, configs of logs te verifiëren is.

## Pipedrive v1 → v2 migratie
- Gebruik `docs/PIPEDRIVE_V1_TO_V2_MIGRATION_PLAYBOOK.md` als canonieke interne bron.
- Als andere repo-notes of oudere handoff-docs hiermee conflicteren, volg dan dit playbook en verifieer tegen officiële Pipedrive docs.
- Werk fail-closed:
  - geen impliciete v1/v2 fallback;
  - geen aannames over pagination per versie;
  - geen claims zonder verificatie in code, docs, OpenAPI of testoutput.

## Werkwijze
- Inspecteer eerst, maak dan de kleinste gerichte wijziging, verifieer daarna.
- Centraliseer migratielogica aan de integratiegrens waar mogelijk.
- Houd business policy gescheiden van API-contractmigratie.
- Maak echte voortgang; stop niet na alleen analyse als implementatie mogelijk is.

## Verificatie
- Voor runtimewijzigingen: draai de kleinste relevante checks/tests voor de gewijzigde paden.
- Claim alleen dat iets werkt als het is geverifieerd.
- Bij falende checks: fixen en opnieuw draaien voordat je afrondt.

## Veiligheid
- Commit of log nooit secrets.
- Vraag vooraf toestemming voor destructieve acties, productie-impact, of onomkeerbare opschoonacties.
