# BMAD Bundle Repo Tooling Template

Dit is de standaard repo-tooling pack voor `/skill:bmad-bundle`.

## Inhoud

- `scripts/bmad_bundle.py` — Codex-friendly BMAD runner
- `scripts/quality_gates.py` — stabiele entrypoint naar repo-native gates
- `scripts/check_file_limits.py` — stabiele entrypoint naar file-limit gate
- `tools/bmad/**` — story proof + Ralph backlog verify
- `tools/guard/gates.py` — JSON-gedreven quality-gate runner
- `tools/guard/quality_gates.json` — repo-specifieke gate-config
- `tools/guard/file_limits_gate.py` — fail-closed 300/20 file-limit gate
- `tools/guard/file_limits_allowlist.json` — legacy baseline uitzonderingen

## Na bootstrap altijd doen

1. Pas `tools/guard/quality_gates.json` aan op de echte repo-commands.
2. Run `python3 scripts/check_file_limits.py`.
3. Leg bestaande legacy overtredingen vast in `tools/guard/file_limits_allowlist.json` zonder de globale 300/20 limieten te verruimen.
4. Smoke-test:
   - `python3 scripts/bmad_bundle.py --help`
   - `python3 scripts/check_file_limits.py`
5. Commit de bootstrap voordat je RUN2 start.

## Standaard gate-config

De meegeleverde `quality_gates.json` gaat uit van een Node/OpenSpec repo met:

- `openspec validate --all --strict --no-interactive`
- `npm run lint`
- `npm run typecheck`
- `npm run test:all`

Als het target repo daarvan afwijkt, moet de config direct worden aangepast vóór gebruik.
