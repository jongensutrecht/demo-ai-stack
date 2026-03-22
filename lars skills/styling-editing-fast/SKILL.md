---
name: styling-editing-fast
description: Fast visual styling edits for existing UI code. Use when the user wants quick CSS/className/theme tweaks, exact visual matching between components, or rapid iteration without exploratory redesign.
allowed-tools: read edit write bash
---

# Styling Editing Fast

Use this skill when the goal is **speed + exactness** for UI styling work.

## Core rule

Do **not** redesign.
Do **not** brainstorm variants.
Do **not** explain long chains of reasoning.
Do **not** deliver lazy polish without proof.

Instead:
1. Find the exact source element the user points to.
2. Find the exact target element to change.
3. Compare the current classes/styles.
4. Copy the source styling **1:1** when asked for "same as".
5. Only change the explicitly requested delta (for example: color, radius, label text, spacing).
6. Capture proof.

## 10/10-kader voor snelle styling-edits

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Styling-specifiek:

- "zelfde als X" betekent 1-op-1 class/token-vergelijking, niet "ongeveer"
- diff blijft klein, lokaal en zonder creatieve scope-uitbreiding
- before/after bewijs is verplicht bij visuele changes

## Default operating mode

When the user says things like:
- "maak deze knop zoals die knop"
- "zelfde stijl als ..."
- "zelfde kleur/felheid/radius"
- "snelle styling tweak"
- "niet al dat reasoning gedoe"

then follow this protocol.

## Fast protocol

### A. Exact-match requests

For requests like "make A like B":
- Read the file containing **B**.
- Read the file containing **A**.
- Extract the exact className/style/token values.
- Replace A with B's styling directly.
- Keep only the explicitly requested differences.

Allowed difference examples:
- same classes, different text
- same classes, different color family
- same classes, different radius
- same classes, no blur

### B. Small styling tweak requests

For requests like:
- "meer amber"
- "letters feller"
- "rand geler"
- "radius 3"

make the **smallest possible edit** in the most local place.
Do not refactor unless required.

### C. User frustration mode

If the user is clearly frustrated:
- Stop proposing options.
- Stop interpreting intent broadly.
- Apply the most literal reading of the request.
- Report only:
  - what changed
  - file path
  - proof screenshot/log if relevant

## Rules for class-based UIs

When working with Tailwind / className strings:
- Prefer copying the full class string from source to target.
- Avoid recomposing the same style from memory.
- If only one token differs, edit only that token.
- Keep order stable when possible to reduce diff noise.

## Rules for tokens/CSS variables

If the change is token-level:
- change the token once
- then verify the affected screens
- do not mix token changes with unrelated component tweaks in the same pass

## Verification

After every visible styling change:
1. Run the smallest relevant lint/check if code changed.
2. Capture a screenshot of the affected UI.
3. If the user asked for "same as X", verify by re-reading both source and target class strings.

## Output style

Be brief.
Use this format:
- Changed: <what>
- File: <path>
- Verified: <screenshot/test>

## Anti-patterns

Do not:
- invent "better" styles the user did not ask for
- broaden the scope to surrounding components unless asked
- keep cycling through variants when the request is specific
- say "it should now match" without checking the actual classes
- deliver a generic cleanup/polish diff without a concrete requested visual outcome
- treat a screenshot as optional after a visible change

## Good example

User: "Maak Toevoegen exact zoals Open bij Projects."

Correct behavior:
- read source button classes in Projects
- read target button classes in Improve
- copy classes 1:1
- preserve only necessary differences like `type="submit"` and `disabled={...}`
- capture screenshot

## When to ask a question

Ask only if there are **multiple possible source elements** and it is genuinely ambiguous.
Otherwise, choose the most literal source/target pair and execute.
