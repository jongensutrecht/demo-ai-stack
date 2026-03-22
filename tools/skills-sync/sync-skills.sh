#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: sync-skills.sh [--from-repo|--from-claude] [--apply]

Default behavior:
  - source of truth = repo/skills
  - mode = dry-run

Flags:
  --from-repo    Sync from repo/skills -> ~/.claude/skills (default)
  --from-claude  Sync from ~/.claude/skills -> repo/skills
  --apply        Perform the sync (without this flag the script is dry-run only)
  -h, --help     Show this help
USAGE
}

mode="from-repo"
apply="false"

for arg in "$@"; do
  case "$arg" in
    --from-repo)
      mode="from-repo"
      ;;
    --from-claude)
      mode="from-claude"
      ;;
    --apply)
      apply="true"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $arg" >&2
      usage
      exit 2
      ;;
  esac
done

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
repo_skills="${repo_root}/skills"
claude_skills="${HOME}/.claude/skills"
backup_root="${repo_root}/artifacts/backups"
timestamp="$(date +%Y%m%d_%H%M%S)"

if [ ! -d "$repo_skills" ]; then
  echo "Missing repo skills folder: $repo_skills" >&2
  exit 1
fi

if [ ! -d "$claude_skills" ]; then
  echo "Missing Claude skills folder: $claude_skills" >&2
  exit 1
fi

if [ "$mode" = "from-repo" ]; then
  src="${repo_skills}/"
  dest="${claude_skills}/"
else
  src="${claude_skills}/"
  dest="${repo_skills}/"
fi

rsync_args=( -a --delete --exclude '.git' )
if [ "$apply" != "true" ]; then
  rsync_args+=( --dry-run )
  echo "[INFO] Dry-run mode (add --apply to perform changes)"
else
  mkdir -p "$backup_root"
  backup_tar="${backup_root}/skills-sync_${mode}_${timestamp}.tar.gz"
  tar -czf "$backup_tar" -C "$dest" .
  echo "[INFO] Backup created: $backup_tar"
fi

echo "[INFO] source: $src"
echo "[INFO] destination: $dest"
rsync "${rsync_args[@]}" "$src" "$dest"

echo "[OK] skills sync completed"
