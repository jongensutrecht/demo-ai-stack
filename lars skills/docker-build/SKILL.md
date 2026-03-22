---
name: docker-build
description: "REPO-SPECIFIEK: Build/deploy van de Offerte Docker service (aanvraag_offerte). Niet generiek - werkt alleen voor die ene service."
---

# Docker Build - Offerte only

> **Let op:** deze skill is specifiek voor `aanvraag_offerte` / `jvdp-offerte`. Voor andere repos met Docker: gebruik gewoon `docker compose build` of het repo-eigen deploy script.

Use this skill when you need a **manual build/deploy** that still enforces the full local quality gates.

## 10/10-kader

Universele guards: zie `~/.pi/agent/skills/_guards.md`. Docker-specifiek: verify/gates eerst, build/deploy daarna. Succesclaim pas na gate + build + exitstatus bewijs.

## Prereqs

- Run from the repo root.
- `scripts/verify.sh` and `scripts/deploy.sh` are present and executable.
- For remote deploys, ensure SSH access to `jvdp` (override with `DEPLOY_HOST`).

## Local build (no deploy)

```bash
./scripts/verify.sh
docker compose build offerte
```

## Manual deploy (rsync + docker compose)

```bash
./scripts/deploy.sh
```

### Deploy overrides

```bash
DEPLOY_HOST=jvdp \
DEPLOY_APP_PATH=/opt/apps/aanvraag_offerte \
DEPLOY_INFRA_PATH=/opt/infra \
DEPLOY_SERVICE=offerte \
RSYNC_PATH="sudo rsync" \
./scripts/deploy.sh
```

## Notes

- `scripts/deploy.sh` **always** runs `scripts/verify.sh` first. If gates fail, deploy stops.
- Manual `docker build` / `docker compose` bypasses gates unless you run `scripts/verify.sh` first.
- Universele guards: zie `~/.pi/agent/skills/_guards.md`. Rapporteer commands, exitstatus en bewijs.
