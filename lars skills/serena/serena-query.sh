#!/usr/bin/env bash
# Serena CLI wrapper — calls the project server HTTP API
# Usage: serena-query.sh <project_name> <tool_name> '<json_params>'
# Example: serena-query.sh photobooth_project_claude find_symbol '{"name": "PlannerEngine"}'

set -euo pipefail

SERENA_PORT="${SERENA_PORT:-34200}"
SERENA_HOST="${SERENA_HOST:-127.0.0.1}"
PROJECT="${1:?Usage: serena-query.sh <project> <tool> [params_json]}"
TOOL="${2:?Usage: serena-query.sh <project> <tool> [params_json]}"
PARAMS="${3:-\{\}}"

# Check server is running
if ! lsof -i ":${SERENA_PORT}" >/dev/null 2>&1; then
  echo "ERROR: Serena server not running on port ${SERENA_PORT}" >&2
  echo "Start it: tmux new-session -d -s serena 'serena start-project-server --port ${SERENA_PORT}'" >&2
  exit 1
fi

export _SQ_PROJECT="$PROJECT"
export _SQ_TOOL="$TOOL"
export _SQ_PARAMS="$PARAMS"
export _SQ_HOST="$SERENA_HOST"
export _SQ_PORT="$SERENA_PORT"

python3 << 'PYEOF'
import json, http.client, sys, os

project = os.environ["_SQ_PROJECT"]
tool = os.environ["_SQ_TOOL"]
params_raw = os.environ["_SQ_PARAMS"]

params = json.loads(params_raw)
body = json.dumps({
    "project_name": project,
    "tool_name": tool,
    "tool_params_json": json.dumps(params)
})

conn = http.client.HTTPConnection(os.environ.get("_SQ_HOST", "127.0.0.1"), int(os.environ.get("_SQ_PORT", "34200")))
conn.request("POST", "/query_project", body, {"Content-Type": "application/json"})
resp = conn.getresponse()
data = resp.read().decode()
if resp.status != 200:
    print(f"ERROR ({resp.status}): {data}", file=sys.stderr)
    sys.exit(1)
print(data)
PYEOF
