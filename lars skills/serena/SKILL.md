---
name: serena
description: Semantische code navigatie via LSP — vind symbolen, referenties, en edit op symboolniveau. Gebruik voor grote codebases waar grep niet genoeg is.
allowed-tools: Read, Bash
user-invocable: true
---

# Serena (CLI)

Serena geeft IDE-achtige code navigatie via LSP. In plaats van hele files lezen of grep, werk je op symboolniveau.

## Setup

Serena draait als project server op port 34200. Alle queries gaan via het wrapper script.

**Server starten** (eenmalig per sessie):
```bash
tmux new-session -d -s serena 'serena start-project-server --port 34200'
```

**Check of server draait:**
```bash
tmux has-session -t serena 2>/dev/null && echo "running" || echo "not running"
lsof -i :34200
```

**Query wrapper:**
```bash
~/.pi/agent/skills/serena/serena-query.sh <project> <tool> '<json_params>'
```

## Geconfigureerde projecten

| Project | Pad | Taal |
|---------|-----|------|
| photobooth_project_claude | ~/dev/github.com/jongensutrecht/photobooth_project_claude | Python |

Meer projecten toevoegen:
```bash
serena project create <pad> --name <naam> --language <taal> --index
```

## Correcte parameternamen per tool

Dit zijn de exacte signatures (geverifieerd tegen serena-agent 0.1.4):

| Tool | Vereiste params | Optionele params |
|------|----------------|------------------|
| `find_symbol` | `name_path_pattern` | `depth`, `relative_path`, `include_body`, `include_info`, `substring_matching` |
| `find_referencing_symbols` | `name_path`, `relative_path` | `include_kinds`, `exclude_kinds` |
| `get_symbols_overview` | `relative_path` | `depth` |
| `rename_symbol` | `name_path`, `relative_path`, `new_name` | — |
| `replace_symbol_body` | `name_path`, `relative_path`, `body` | — |
| `search_for_pattern` | `substring_pattern` | `context_lines_before`, `context_lines_after`, `relative_path`, `paths_include_glob`, `paths_exclude_glob` |

**Let op het verschil:**
- `find_symbol` gebruikt `name_path_pattern`
- `find_referencing_symbols` / `rename_symbol` / `replace_symbol_body` gebruiken `name_path` (zonder _pattern)

## Veelgebruikte queries

### Vind een symbool (functie, class, variabele)
```bash
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude find_symbol \
  '{"name_path_pattern": "MyClass"}'

# Met diepte (children ophalen, bijv. methods van een class)
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude find_symbol \
  '{"name_path_pattern": "MyClass", "depth": 1}'

# Met body (code ophalen)
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude find_symbol \
  '{"name_path_pattern": "my_function", "include_body": true}'

# Substring matching
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude find_symbol \
  '{"name_path_pattern": "planner", "substring_matching": true}'
```

### Vind wie een symbool gebruikt (referenties)
```bash
# LET OP: hier is het "name_path", NIET "name_path_pattern"
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude find_referencing_symbols \
  '{"relative_path": "src/core/engine.py", "name_path": "process_image"}'
```

### Overzicht van symbolen in een file
```bash
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude get_symbols_overview \
  '{"relative_path": "main.py"}'

# Met diepte (ook methods van classes tonen)
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude get_symbols_overview \
  '{"relative_path": "main.py", "depth": 1}'
```

### Zoek een patroon (zoals grep maar project-aware)
```bash
# LET OP: parameter heet "substring_pattern", niet "pattern"
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude search_for_pattern \
  '{"substring_pattern": "TODO|FIXME"}'
```

### Hernoem een symbool overal
```bash
# LET OP: "name_path", niet "name_path_pattern"
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude rename_symbol \
  '{"relative_path": "src/module.py", "name_path": "old_name", "new_name": "new_name"}'
```

### Vervang de body van een functie
```bash
# LET OP: "name_path" en "body", niet "name_path_pattern" en "new_body"
~/.pi/agent/skills/serena/serena-query.sh photobooth_project_claude replace_symbol_body \
  '{"relative_path": "src/module.py", "name_path": "my_function", "body": "def my_function():\n    return 42"}'
```

## Herindexeren

Na grote wijzigingen:
```bash
serena project index <pad>
```

## Tips

- `find_symbol` met `substring_matching: true` is handig als je de exacte naam niet weet
- `get_symbols_overview` is het eerste wat je doet bij een onbekend bestand
- `depth: 1` op find_symbol/get_symbols_overview toont ook methods van classes
- Gebruik Serena NAAST de gewone Pi tools (read, grep, edit) — niet als vervanging
- Server hoeft maar 1x gestart; blijft draaien in tmux
- **Parameternamen verschillen per tool** — check de tabel hierboven als je twijfelt
