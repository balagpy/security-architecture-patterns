#!/usr/bin/env bash
set -euo pipefail

VULN="http://localhost:8101"
MIT="http://localhost:8102"

echo "[1/5] Starting lab"
docker compose up --build -d

echo "[2/5] Waiting for health"
for i in {1..30}; do
  if curl -fsS "$VULN/health" >/dev/null && curl -fsS "$MIT/health" >/dev/null; then
    break
  fi
  sleep 1
done

echo "[3/5] Issue Tenant-A token"
TOKEN_A=$(curl -s -X POST "$VULN/issue" -H 'content-type: application/json' -d '{"tenant_id":"tenant-a","user":"alice"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')

echo "[4/5] Request invoice 42 using Tenant-A token"
echo "vulnerable service response:"
curl -s "$VULN/invoice/42" -H "Authorization: Bearer $TOKEN_A" && echo

echo "mitigated service response:"
curl -s "$MIT/invoice/42" -H "Authorization: Bearer $TOKEN_A" && echo

echo "[5/5] Interpretation"
echo "If vulnerable returns data.tenant_id=tenant-b, cross-tenant leak is reproduced."
