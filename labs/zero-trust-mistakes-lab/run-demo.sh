#!/usr/bin/env bash
set -euo pipefail

A_V="http://localhost:8611"
A_M="http://localhost:8612"

echo "[1/5] Starting lab"
docker compose up --build -d

echo "[2/5] Waiting for health"
for i in {1..30}; do
  if curl -fsS "http://localhost:8602/health" >/dev/null && curl -fsS "http://localhost:8603/health" >/dev/null && curl -fsS "$A_V/health" >/dev/null && curl -fsS "$A_M/health" >/dev/null; then
    break
  fi
  sleep 1
done

echo "[3/5] Lateral move to vulnerable service-b without workload token"
curl -s "$A_V/pivot" && echo

echo "[4/5] Same attempt to mitigated service-b without token (should fail)"
curl -s "$A_M/pivot" && echo

echo "Now present valid workload token to mitigated path (should pass)"
curl -s "$A_M/pivot?token=trusted-a-token" && echo

echo "[5/5] Interpretation"
echo "If vulnerable allows anonymous east-west and mitigated requires workload identity, zero-trust gap is demonstrated."
