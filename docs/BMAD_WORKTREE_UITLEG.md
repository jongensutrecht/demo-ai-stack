# BMAD Worktree Structuur

## Overzicht

Elke BMAD process krijgt een **overkoepelende worktree folder** genoemd naar het `bmad_input/*.md` bestand. Stories worden ontwikkeld in **geïsoleerde story worktrees** en gemerged in een **dedicated merge worktree**.

---

## Folder Structuur

```
worktrees_claude/
└── <PROCESS>/                    ← Overkoepelende folder (slug van bmad_input bestand)
    ├── main-merge/               ← Merge worktree (ENIGE plek waar merge gebeurt)
    │   └── [merge branch: merge-<PROCESS>]
    ├── <STORY_ID_1>/             ← Story worktree 1
    │   └── [story branch: story-<id>]
    ├── <STORY_ID_2>/             ← Story worktree 2
    │   └── [story branch: story-<id>]
    └── <STORY_ID_3>/             ← Story worktree 3
        └── [story branch: story-<id>]
```

---

## Voorbeeld

**Input:** `bmad_input/nav-overhaul.md`

**Resulteert in:**

```
worktrees_claude/
└── nav_overhaul/                 ← PROCESS = slug("nav-overhaul.md")
    ├── main-merge/               ← Merge worktree
    │   └── [branch: merge-nav_overhaul]
    ├── NAV-01/                   ← Story: TopHeader
    │   └── [branch: story-nav-01]
    ├── NAV-02/                   ← Story: SlideoutMenu
    │   └── [branch: story-nav-02]
    └── NAV-03/                   ← Story: AppShell Refactor
        └── [branch: story-nav-03]
```

---

## Workflow

### 1. Setup (Eenmalig per Process)

```bash
# Bepaal process naam
PROCESS="nav_overhaul"  # slug van bmad_input bestandsnaam

# Maak merge worktree
WT_ROOT="worktrees_claude/${PROCESS}"
MERGE_WT="${WT_ROOT}/main-merge"

git worktree add -b "merge-${PROCESS}" "$MERGE_WT" origin/main
```

---

### 2. Per Story

```bash
# Variabelen
STORY_ID="NAV-01"
BRANCH="story-${STORY_ID,,}"      # story-nav-01
STORY_WT="${WT_ROOT}/${STORY_ID}" # worktrees_claude/nav_overhaul/NAV-01

# Maak story worktree
git worktree add -b "$BRANCH" "$STORY_WT" origin/main

# Ga naar story worktree
cd "$STORY_WT"

# Verifieer isolatie
git branch --show-current  # moet $BRANCH zijn
pwd                        # moet $STORY_WT zijn

# Werk aan de story...
# ... implementatie ...
# ... tests ...
# ... commit ...
```

---

### 3. Merge (Alleen in main-merge)

```bash
# Ga naar merge worktree
cd "$MERGE_WT"  # worktrees_claude/nav_overhaul/main-merge

# Merge story
git merge --no-ff "$BRANCH" -m "feat($STORY_ID): <titel>"

# Voorbeeld:
# git merge --no-ff "story-nav-01" -m "feat(NAV-01): TopHeader component"
```

---

### 4. Cleanup (Na merge)

```bash
# Verwijder story worktree
git worktree remove "$STORY_WT"

# Verwijder story branch
git branch -d "$BRANCH"
```

---

## Regels

### ✅ VERPLICHT

- **Overkoepelende folder** = slug van `bmad_input/<naam>.md`
- **Elke story** = eigen worktree in `${WT_ROOT}/${STORY_ID}/`
- **Mergen** = ALLEEN in `${WT_ROOT}/main-merge/`
- **Isolatie** = Geen story mag code van andere story zien tijdens development

### ❌ VERBODEN

- Direct committen op `main` voor story werk
- Mergen in de hoofdrepo (alleen in `main-merge/`)
- Meerdere stories in 1 worktree
- Worktree stap overslaan "omdat het sneller is"

---

## Process Naam Bepaling

```python
def slug(filename: str) -> str:
    """
    Converteer bmad_input bestandsnaam naar process naam.

    Voorbeeld:
      nav-overhaul.md     → nav_overhaul
      dark-mode-toggle.md → dark_mode_toggle
      API Setup.md        → api_setup
    """
    # 1. Strip extensie
    name = filename.replace('.md', '')

    # 2. Lowercase
    name = name.lower()

    # 3. Vervang non-alphanumeric met underscore
    name = re.sub(r'[^a-z0-9]+', '_', name)

    # 4. Trim underscores aan begin/eind
    name = name.strip('_')

    return name
```

---

## Verificatie

```bash
# Check worktrees
git worktree list

# Verwacht output:
# /pad/naar/repo                        abc123 [main]
# /pad/naar/worktrees_claude/nav_overhaul/main-merge  def456 [merge-nav_overhaul]
# /pad/naar/worktrees_claude/nav_overhaul/NAV-01      ghi789 [story-nav-01]
# /pad/naar/worktrees_claude/nav_overhaul/NAV-02      jkl012 [story-nav-02]

# Check isolatie (in story worktree)
cd worktrees_claude/nav_overhaul/NAV-01
git branch --show-current  # → story-nav-01
git log --oneline -5       # → alleen NAV-01 commits
```

---

## Voordelen

| Voordeel | Uitleg |
|----------|--------|
| **Volledige isolatie** | Story A ziet geen code van story B tijdens development |
| **Parallelle development** | Meerdere stories tegelijk (in subprocesses) |
| **Clean merge history** | Alle merges gebeuren in dedicated merge worktree |
| **Easy rollback** | Per story branch = makkelijk terugdraaien |
| **Process grouping** | Alle stories van 1 process bij elkaar |

---

## Gerelateerd

- `/bmad-bundle` - Gebruikt deze worktree structuur
- `skills/bmad-bundle/SKILL.md` - Volledige skill definitie
- `AI_STACK_STANDARD_BMAD_WORKTREES_GUARDRAILS.md` - Gedetailleerde guardrails
