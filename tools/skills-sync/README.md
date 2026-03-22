# Skills Sync

Doel: houd de canonieke repo-skills en `~/.claude/skills` synchroon, zonder destructieve defaults.

## Canonieke bron

- **SSOT:** `repo/skills`
- `.claude/skills` is de lokale distributiedoelmap

## Gebruik

### Veilige dry-run (default)
```bash
./tools/skills-sync/sync-skills.sh
```

### Echt toepassen vanuit repo naar lokale Claude skills
```bash
./tools/skills-sync/sync-skills.sh --apply
```

### Omgekeerd syncen (alleen expliciet)
```bash
./tools/skills-sync/sync-skills.sh --from-claude --apply
```

## Veiligheid

- Zonder `--apply` gebeurt **geen** echte wijziging
- Bij `--apply` wordt eerst een timestamped backup van de bestemming gemaakt
- `rsync --delete` blijft krachtig; gebruik `--from-claude --apply` alleen als je bewust de repo wilt bijwerken vanuit je lokale mirror
