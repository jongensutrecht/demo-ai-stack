# Demo AI Stack FILE_LIMITS_EXCEPTIONS

Dit bestand is de **SSOT allowlist** voor file-limit uitzonderingen.

Regels:
- Alleen toevoegen als splitten nu niet redelijk is
- Elke uitzondering heeft `path`, `reason`, `category`, `owner` en óf `expires_on` óf `never_expires`
- Uitzonderingen zonder rationale horen door de gate te falen

```json
[
  {
    "path": "docs/UNIVERSAL_CTO_REPO_SCAN_PROMPT_v2.md",
    "reason": "Canonieke long-form audit prompt; bewust compact gemaakt maar nog steeds een contract-document.",
    "category": "contract_doc",
    "owner": "repo-governance",
    "never_expires": true
  },
  {
    "path": "docs/CTO_RULES.md",
    "reason": "Canonieke registry met rule IDs + DoD + verificatie; append-only YAML block maakt deze file langer dan 300 regels.",
    "category": "contract_doc",
    "owner": "repo-governance",
    "never_expires": true
  },
  {
    "path": "skills/bmad-bundle/SKILL.md",
    "reason": "Bundled workflow skill; opsplitsing gepland maar nog canoniek in huidige distributie.",
    "category": "workflow_skill",
    "owner": "repo-governance",
    "expires_on": "2026-06-30"
  },
  {
    "path": "tools/test-gate/test-gate.ps1",
    "reason": "Legacy PowerShell implementation; function-count ok maar line-count boven limiet.",
    "category": "legacy_tooling",
    "owner": "tooling",
    "expires_on": "2026-06-30"
  },
  {
    "path": "tools/test-gate/test-gate.sh",
    "reason": "Legacy bash implementation; line-count boven limiet.",
    "category": "legacy_tooling",
    "owner": "tooling",
    "expires_on": "2026-06-30"
  },
  {
    "path": "tools/invariant-check/invariant-check.ps1",
    "reason": "Legacy PowerShell implementation; line-count boven limiet.",
    "category": "legacy_tooling",
    "owner": "tooling",
    "expires_on": "2026-06-30"
  },
  {
    "path": "tools/invariant-check/invariant-check.sh",
    "reason": "Legacy bash implementation; line-count boven limiet.",
    "category": "legacy_tooling",
    "owner": "tooling",
    "expires_on": "2026-06-30"
  },
  {
    "path": "tools/preflight/preflight.ps1",
    "reason": "Legacy exported preflight script; line-count boven limiet.",
    "category": "legacy_tooling",
    "owner": "tooling",
    "expires_on": "2026-06-30"
  },
  {
    "path": "tools/story-runner/story_runner.py",
    "reason": "Story runner blijft tijdelijk één file; split gepland na safety-hardening.",
    "category": "legacy_tooling",
    "owner": "tooling",
    "expires_on": "2026-06-30"
  },
  {
    "path": "bmad_autopilot_kit/AI_STACK_STANDARD_BMAD_WORKTREES_GUARDRAILS seq force_claude.md",
    "reason": "Exported contract/playbook artefact; naam en lengte volgen legacy kit formaat.",
    "category": "exported_contract",
    "owner": "kit",
    "never_expires": true
  },
  {
    "path": "bmad_autopilot_kit/tools_claude/bmad-story-preflight_claude/preflight_claude.ps1",
    "reason": "Exported kit-script; lengte volgt huidige downstream compatibiliteit.",
    "category": "exported_tool",
    "owner": "kit",
    "never_expires": true
  },
  {
    "path": "lars skills/**",
    "reason": "Legacy mirror-map; niet canoniek en standaard uit default search/gates gehouden.",
    "category": "legacy_mirror",
    "owner": "repo-governance",
    "never_expires": true
  }
]
```
