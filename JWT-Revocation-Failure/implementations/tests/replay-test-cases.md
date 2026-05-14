# Replay Test Cases

1. Revoke token and replay immediately across all replicas.
2. Inject revocation backend latency and verify route policy behavior.
3. Validate mixed-version rollout does not re-enable revoked tokens.
