# Security Policy

## Reporting

Meld kwetsbaarheden niet via publieke issues als de impact nog onbekend is.

Gebruik één van deze routes:
- open een private security advisory als dat platformmatig beschikbaar is
- of neem direct contact op met de maintainer van dit project via het afgesproken private kanaal

## Wat wij minimaal verwachten

- geen secrets in git
- fail-closed gedrag bij onveilige of incomplete configuratie
- expliciete opt-in voor destructieve acties
- duidelijke waarschuwingen bij execution van onbetrouwbare input

## Scope

Deze repo bevat vooral tooling, skills, prompts en governance-documenten. Security-risico's zitten daarom vooral in:
- shell/command execution
- sync- en delete-scripts
- doc/tooling drift waardoor unsafe defaults ontstaan

## Responsible disclosure

Geef waar mogelijk mee:
- impact
- reproduceerbare stappen
- relevante file paths en commit/SHA
- suggested mitigation als je die hebt
