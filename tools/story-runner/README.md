# Story runner

Run a process:
- `python tools/story-runner/story_runner.py show --process docs/processes/cto_repo_scan_2026_01/PROCESS.md`
- `python tools/story-runner/story_runner.py verify --process docs/processes/cto_repo_scan_2026_01/PROCESS.md`

JSON output:
- `python tools/story-runner/story_runner.py verify --process docs/processes/cto_repo_scan_2026_01/PROCESS.md --json-output artifacts/debug/story-runner.json`

## Formats ondersteund

- Story IDs: `PREFIX-001` en `PREFIX.001`
- Verification regels:
  - `- **Verification (repo-root):** \`...\``
  - `- Verification (cwd=path): \`...\``
  - Legacy zonder bold is toegestaan
- Expected:
  - `exit code N` (case-insensitive) → exitcode match
  - anders → substring match in stdout/stderr
