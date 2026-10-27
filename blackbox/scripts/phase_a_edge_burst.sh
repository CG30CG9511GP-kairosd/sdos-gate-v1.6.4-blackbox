#!/bin/bash
set -euo pipefail
BASE="${SDOS_BASE:-http://127.0.0.1:8000}"
N="${BURST_N:-80}"
INSECURE="${CURL_INSECURE:-0}"
OPTS=(-s -o /dev/null -w "%{http_code}\n")
[[ "$INSECURE" == "1" ]] && OPTS+=(-k)
echo "BASE=$BASE N=$N"
for path in /health /ready; do
  echo "== $path =="
  for i in $(seq 1 "$N"); do curl "${OPTS[@]}" "$BASE$path" || echo err; done | sort | uniq -c
done
echo "NOTA: Gate directo => health/ready sin 429 proceso. Edge nginx => posible 429."
