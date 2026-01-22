# Skills Sync

Doel: houd de skills in deze repo en in `~/.claude/skills` identiek.

## Gebruik

```bash
./tools/skills-sync/sync-skills.sh
```

## Richting

- Default: `~/.claude/skills` -> `repo/skills`
- Omgekeerd:

```bash
./tools/skills-sync/sync-skills.sh --from-repo
```

## Veiligheid

- `rsync --delete` maakt de bestemming exact gelijk aan de bron.
- Gebruik `--dry-run` om eerst te zien wat er verandert.
