#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: $0 <port> [label]" >&2
  exit 64
fi

PORT="$1"
LABEL="${2:-service}"

find_listeners() {
  lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null || true
}

PIDS="$(find_listeners)"
if [[ -z "$PIDS" ]]; then
  echo "PORT_FREE $PORT $LABEL"
  exit 0
fi

echo "PORT_OCCUPIED $PORT $LABEL"
while IFS= read -r pid; do
  [[ -n "$pid" ]] || continue
  ps -p "$pid" -o pid=,user=,comm=,args=
done <<< "$PIDS"

while IFS= read -r pid; do
  [[ -n "$pid" ]] || continue
  kill "$pid" 2>/dev/null || true
done <<< "$PIDS"

for _ in $(seq 1 25); do
  sleep 0.2
  if [[ -z "$(find_listeners)" ]]; then
    echo "PORT_FREED $PORT $LABEL"
    exit 0
  fi
done

PIDS="$(find_listeners)"
while IFS= read -r pid; do
  [[ -n "$pid" ]] || continue
  kill -9 "$pid" 2>/dev/null || true
done <<< "$PIDS"

sleep 0.2
if [[ -n "$(find_listeners)" ]]; then
  echo "PORT_STILL_OCCUPIED $PORT $LABEL" >&2
  exit 1
fi

echo "PORT_FREED_FORCE $PORT $LABEL"
