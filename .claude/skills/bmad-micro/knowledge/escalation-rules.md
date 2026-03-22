# BMAD Micro Escalation Rules

Gebruik **niet** BMAD Micro als één van deze klopt:

- je hebt een migration/schema change nodig
- je raakt authn/authz of publieke API-shapes
- je wijzigt infra/deploy/CI gedrag
- je moet meerdere subsystemen tegelijk aanraken
- je verwacht >120 netto wijzigingsregels
- je moet eerst een grotere cleanup/refactor doen om het netjes te krijgen

Dan geldt:
- gebruik `/plan-to-bmad`
- daarna `/bmad-bundle`

Doel van BMAD Micro:
- kleine wijziging
- hoge kwaliteitslat
- minimale overhead
- **geen** massive refactor achteraf
