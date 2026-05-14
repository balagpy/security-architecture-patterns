# jwt-revocation-lab

This lab demonstrates why JWT revocation fails in distributed systems when services rely on stale local revocation caches, and how centralized synchronous checks mitigate the gap.

## Architecture

- `api-a` (`:8001`) and `api-b` (`:8002`) run in `vulnerable` mode.
- `api-mitigated` (`:8003`) runs in `mitigated` mode.
- `redis` stores authoritative revoked token IDs (`jti`).

Vulnerable mode behavior:
- each instance refreshes revocation state every 20 seconds
- revoked token may still pass until next refresh

Mitigated mode behavior:
- every request checks Redis for revoked `jti`
- revocation enforcement is immediate (subject to Redis availability)

## Run

```bash
docker compose up --build
```

## Demo Steps

1. Issue a token from `api-a`:
```bash
TOKEN=$(curl -s -X POST http://localhost:8001/issue -H 'content-type: application/json' -d '{"sub":"alice"}' | python3 -c 'import sys, json; print(json.load(sys.stdin)["token"])')
```

2. Access resource on both vulnerable instances:
```bash
curl -s http://localhost:8001/resource -H "Authorization: Bearer $TOKEN"
curl -s http://localhost:8002/resource -H "Authorization: Bearer $TOKEN"
```

3. Revoke token through `api-a`:
```bash
curl -s -X POST http://localhost:8001/revoke -H "Authorization: Bearer $TOKEN"
```

4. Immediately replay token:
```bash
curl -s http://localhost:8001/resource -H "Authorization: Bearer $TOKEN"
curl -s http://localhost:8002/resource -H "Authorization: Bearer $TOKEN"
curl -s http://localhost:8003/resource -H "Authorization: Bearer $TOKEN"
```

Expected:
- `api-a`/`api-b` may still allow during stale-cache window.
- `api-mitigated` should reject immediately.

5. Wait >20 seconds and retry vulnerable endpoints; they should then reject.

## Why This Matters

This models a real-world architecture issue:
- signature validity is checked synchronously
- revocation liveness is checked asynchronously

The exploitability lives in that consistency gap.
