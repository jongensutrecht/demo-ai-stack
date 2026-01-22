#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: sync-skills.sh [--from-claude|--from-repo] [--dry-run]

Default: --from-claude
  --from-claude  Sync from ~/.claude/skills -> repo/skills
  --from-repo    Sync from repo/skills -> ~/.claude/skills
  --dry-run      Show what would change
USAGE
}

mode="from-claude"
dry_run=""

for arg in "$@"; do
  case "$arg" in
    --from-claude)
      mode="from-claude"
      ;;
    --from-repo)
      mode="from-repo"
      ;;
    --dry-run)
      dry_run="--dry-run"
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

if [ ! -d "$repo_skills" ]; then
  echo "Missing repo skills folder: $repo_skills" >&2
  exit 1
fi

if [ ! -d "$claude_skills" ]; then
  echo "Missing Claude skills folder: $claude_skills" >&2
  exit 1
fi

src=""
dest=""
if [ "$mode" = "from-claude" ]; then
  src="${claude_skills}/"
  dest="${repo_skills}/"
else
  src="${repo_skills}/"
  dest="${claude_skills}/"
fi

rsync -a --delete --exclude '.git' $dry_run "$src" "$dest"
