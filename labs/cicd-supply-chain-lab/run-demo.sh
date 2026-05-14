#!/usr/bin/env bash
set -euo pipefail

VULN="http://localhost:8401"
MIT="http://localhost:8402"

echo "[1/5] Starting lab"
docker compose up --build -d

echo "[2/5] Waiting for health"
for i in {1..30}; do
  if curl -fsS "$VULN/health" >/dev/null && curl -fsS "$MIT/health" >/dev/null; then
    break
  fi
  sleep 1
done

echo "[3/5] Test mutable action + unsigned artifact"
PAYLOAD1='{"action_ref":"org/action@v1","artifact_signed":false}'
echo "vulnerable:" && curl -s -X POST "$VULN/evaluate" -H 'content-type: application/json' -d "$PAYLOAD1" && echo
echo "mitigated:" && curl -s -X POST "$MIT/evaluate" -H 'content-type: application/json' -d "$PAYLOAD1" && echo

echo "[4/5] Test pinned action + signed artifact"
PAYLOAD2='{"action_ref":"org/action@1234567890abcdef1234567890abcdef12345678","artifact_signed":true}'
echo "vulnerable:" && curl -s -X POST "$VULN/evaluate" -H 'content-type: application/json' -d "$PAYLOAD2" && echo
echo "mitigated:" && curl -s -X POST "$MIT/evaluate" -H 'content-type: application/json' -d "$PAYLOAD2" && echo

echo "[5/5] Interpretation"
echo "If mitigated blocks payload1 and allows payload2, supply-chain policy hardening is demonstrated."
