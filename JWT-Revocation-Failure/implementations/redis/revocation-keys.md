# Redis Revocation Key Pattern

- Key: `revoked:{jti}`
- Value: `1`
- TTL: `token_exp - now`

Operational note:
- Align key TTL with token lifetime to prevent stale denylist growth.
