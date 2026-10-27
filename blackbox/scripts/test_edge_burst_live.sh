#!/bin/bash
# Vector 6 end-to-end: ráfaga contra el edge nginx → esperar HTTP 429.
# Requiere: docker compose producción-shaped levantado (edge en :443 o :8443).
# Uso:
#   BASE_URL=https://127.0.0.1 CURL_INSECURE=1 ./blackbox/scripts/test_edge_burst_live.sh
set -euo pipefail
BASE_URL="${BASE_URL:-https://127.0.0.1}"
CURL_INSECURE="${CURL_INSECURE:-1}"
N="${BURST_N:-80}"
OPTS=()
if [[ "$CURL_INSECURE" == "1" ]]; then OPTS+=(-k); fi
OPTS+=(-s -o /dev/null -w "%{http_code}")
echo "Burst $N requests against $BASE_URL/v1/gateway/analyze-batch (expect some 429 from edge)"
codes_file=$(mktemp)
for i in $(seq 1 "$N"); do
  curl "${OPTS[@]}" -X POST "$BASE_URL/v1/gateway/analyze-batch" \
    -H "Content-Type: application/json" \
    -d '{}' >>"$codes_file" || true
  echo >>"$codes_file"
done
echo "--- status histogram ---"
sort "$codes_file" | uniq -c | sort -nr
if grep -q '^429$' "$codes_file"; then
  echo "PASS: observed at least one HTTP 429 (edge rate limit)"
  exit 0
fi
echo "FAIL: no HTTP 429 observed. Is nginx edge up with limit_req rate=30r/s?"
echo "Documented alternative: grep rate=30r/s deploy/nginx/nginx.conf"
exit 1
