#!/usr/bin/env bash
set -euo pipefail

BASE_A="http://localhost:8001"
BASE_B="http://localhost:8002"
BASE_M="http://localhost:8003"

echo "[1/6] Building and starting lab..."
docker compose up --build -d

echo "[2/6] Waiting for services..."
for i in {1..30}; do
  if curl -fsS "$BASE_A/health" >/dev/null && curl -fsS "$BASE_B/health" >/dev/null && curl -fsS "$BASE_M/health" >/dev/null; then
    break
  fi
  sleep 1
done

echo "[3/6] Issuing token from api-a..."
TOKEN=$(curl -s -X POST "$BASE_A/issue" -H 'content-type: application/json' -d '{"sub":"alice"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')
echo "Token issued."

echo "[4/6] Baseline access before revocation"
echo "api-a:" && curl -s "$BASE_A/resource" -H "Authorization: Bearer $TOKEN" && echo
echo "api-b:" && curl -s "$BASE_B/resource" -H "Authorization: Bearer $TOKEN" && echo
echo "api-mitigated:" && curl -s "$BASE_M/resource" -H "Authorization: Bearer $TOKEN" && echo

echo "[5/6] Revoking token via api-a"
curl -s -X POST "$BASE_A/revoke" -H "Authorization: Bearer $TOKEN" && echo

echo "Immediate replay (vulnerable may still allow):"
echo "api-a:" && curl -s "$BASE_A/resource" -H "Authorization: Bearer $TOKEN" && echo
echo "api-b:" && curl -s "$BASE_B/resource" -H "Authorization: Bearer $TOKEN" && echo
echo "api-mitigated:" && curl -s "$BASE_M/resource" -H "Authorization: Bearer $TOKEN" && echo

echo "[6/6] Waiting 22s for vulnerable cache refresh..."
sleep 22
echo "Post-refresh replay (all should reject):"
echo "api-a:" && curl -s "$BASE_A/resource" -H "Authorization: Bearer $TOKEN" && echo
echo "api-b:" && curl -s "$BASE_B/resource" -H "Authorization: Bearer $TOKEN" && echo
echo "api-mitigated:" && curl -s "$BASE_M/resource" -H "Authorization: Bearer $TOKEN" && echo

echo "Done."
