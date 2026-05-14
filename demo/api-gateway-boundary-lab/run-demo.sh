#!/usr/bin/env bash
set -euo pipefail

BV="http://localhost:8201"
BM="http://localhost:8202"
GV="http://localhost:8211"
GM="http://localhost:8212"

echo "[1/6] Starting lab"
docker compose up --build -d

echo "[2/6] Waiting for health"
for i in {1..30}; do
  if curl -fsS "$BV/health" >/dev/null && curl -fsS "$BM/health" >/dev/null && curl -fsS "$GV/health" >/dev/null && curl -fsS "$GM/health" >/dev/null; then
    break
  fi
  sleep 1
done

echo "[3/6] Normal path via gateway (admin role)"
echo "gateway->vulnerable backend:"
curl -s "$GV/admin?user=alice&role=admin" && echo
echo "gateway->mitigated backend:"
curl -s "$GM/admin?user=alice&role=admin" && echo

echo "[4/6] Bypass attack: direct call to vulnerable backend with forged header"
curl -s "$BV/admin" -H "X-Role: admin" -H "X-User-Id: attacker" && echo

echo "[5/6] Same bypass attempt to mitigated backend"
curl -s "$BM/admin" -H "X-Role: admin" -H "X-User-Id: attacker" && echo

echo "[6/6] Interpretation"
echo "If vulnerable grants access while mitigated rejects, trust-boundary bypass is reproduced."
