# BMAD Autopilot Kit (copy-to-repo)

Doel: je plakt deze map in de root van een repo, en je plakt daarna alleen `UITVOER_PROMPT.md` in de Codex-agent terminal. De agent doet dan RUN1 -> preflight -> RUN2 en start de sequentiele autopilot **detached** (fail-closed), zodat je terminal vrij blijft.

## Gebruik (kort)

### Optie A: Direct (BMAD input al klaar)
1) Kopieer deze map naar de repo-root als: `bmad_autopilot_kit_codex/`
2) Open `bmad_autopilot_kit_codex/UITVOER_PROMPT.md` en plak die prompt in de agent terminal.

### Optie B: Plan eerst (geen BMAD input)
1) Kopieer deze map naar de repo-root als: `bmad_autopilot_kit_codex/`
2) Open `bmad_autopilot_kit_codex/PLAN_TO_BMAD_PROMPT_codex.md`, vul REQUIREMENT of PLAN_PATH/PLAN_TEXT in, plak in terminal
3) Codex doet onderzoek of plan-transformatie en genereert `bmad_input/<naam>.md`
4) Gebruik output als `BMAD_INPUT_FILE` voor UITVOER_PROMPT

## Contract (single source of truth)

- `docs/CONTRACT.md` (canoniek story-format + parsing markers; tooling/prompts moeten hiermee in sync zijn)

## Wat zit erin

- `PLAN_TO_BMAD_PROMPT_codex.md` (onderzoek + BMAD input generatie - **NIEUW**)
- `UITVOER_PROMPT_codex.md` (main entrypoint - RUN1 → preflight → RUN2)
- `BMAD_STORY_LLM_PLAYBOOK  Seq force_codex.md` (story-structuur + harde regels)
- `AI_STACK_STANDARD_BMAD_WORKTREES_GUARDRAILS seq force_codex.md` (worktree/guardrails)
- `RUN1_STORY_GENERATION_PROMPT.txt`
- `RUN2_RUNNER_IMPLEMENTATION_PROMPT_AUTOEXEC.txt` (gecorrigeerd voor Codex CLI: `codex exec`)
- `RUNBOOK_BMAD_RUN1_RUN2_SOP.md` (menselijke SOP)
- `tools/bmad-story-preflight/` (lint om RUN1 output runner-proof te maken)
- `BMAD_INPUT_TEMPLATE.md` (optionele input file template)
