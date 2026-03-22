# Story runner

Story runner leest een `docs/processes/<process>/PROCESS.md`, resolve't de bijbehorende stories en kan de verification-commando's uitvoeren.

## Veiligheid

**Voer dit alleen uit op vertrouwde story input.**

Story files kunnen arbitraire shell-commando's bevatten. Daarom voert `verify` niets uit zonder expliciete opt-in:
- gebruik `--allow-shell`
- gebruik dit niet op onbetrouwbare of extern aangeleverde stories

## Gebruik

### Story-volgorde tonen
```bash
python tools/story-runner/story_runner.py show --process docs/processes/cto_repo_scan_2026_01/PROCESS.md
```

### Verificaties uitvoeren (expliciete opt-in verplicht)
```bash
python tools/story-runner/story_runner.py verify --process docs/processes/cto_repo_scan_2026_01/PROCESS.md --allow-shell
```

### JSON output
```bash
python tools/story-runner/story_runner.py verify --process docs/processes/cto_repo_scan_2026_01/PROCESS.md --allow-shell --json-output artifacts/debug/story-runner.json
```

## Formats ondersteund

- Story IDs: `PREFIX-001` en `PREFIX.001`
- Verification regels:
  - `- **Verification (repo-root):** \`...\``
  - `- Verification (cwd=path): \`...\``
  - legacy zonder bold is toegestaan
- Expected:
  - `exit code N` → exitcode match
  - anders → substring match in stdout/stderr
