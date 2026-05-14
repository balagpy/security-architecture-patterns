# api-gateway-boundary-lab

This lab demonstrates API gateway trust-boundary failure and a mitigation pattern.

## Components

- `backend-vulnerable` on `:8201`
- `backend-mitigated` on `:8202`
- `gateway-to-vulnerable` on `:8211`
- `gateway-to-mitigated` on `:8212`

## Vulnerable Behavior

Backend trusts `X-Role` header directly. If attacker reaches backend directly, they can forge `X-Role: admin` and get privileged response.

## Mitigated Behavior

Backend requires:
- caller provenance marker (`X-Forwarded-By=gateway`)
- fresh signed identity context (`X-Auth-Signature` over user, role, timestamp)

Direct forged calls fail because signature/provenance validation fails.

## Run

```bash
docker compose up --build
```

Or guided demo:

```bash
./run-demo.sh
```
