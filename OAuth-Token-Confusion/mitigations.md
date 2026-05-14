# Mitigations - OAuth Token Confusion

## Goals

- Enforce strict token intent per endpoint.
- Bind each resource server to explicit issuer and audience policy.
- Remove ambiguous acceptance paths in validation and authorization layers.

## Strategy Comparison

| Strategy | Latency Impact | Complexity | Confusion-Resistance Gain | Scalability |
| --- | --- | --- | --- | --- |
| Strict claim profile validation | Low | Medium | High | High |
| Per-resource audience isolation | Low | Medium | High | Medium-High |
| Centralized middleware + contract tests | Low-Medium | Medium-High | Medium-High | High |
| Scope-action policy binding | Medium | Medium | High | Medium |
| Hybrid (all above) | Medium | High | Very High | Medium-High |

## Pattern Options

1. Strict token profile validation

- Design summary: validate `iss`, `aud`, `exp`, token use, and required claims before policy evaluation.
- Implementation complexity: Medium.
- Performance tradeoff: low request-path overhead.
- Residual risk: legacy client incompatibility during migration.

2. Per-resource-server audience isolation

- Design summary: each API has distinct audience and rejects foreign tokens.
- Implementation complexity: Medium.
- Performance tradeoff: low runtime cost, medium migration effort.
- Residual risk: partial rollout can leave replayable overlap.

3. Centralized validation middleware with contract tests

- Design summary: shared validation library plus endpoint-level policy tests enforced in CI.
- Implementation complexity: Medium-High.
- Performance tradeoff: low runtime overhead, moderate governance overhead.
- Residual risk: custom handlers bypassing shared controls.

4. Scope and action binding

- Design summary: map required scopes to specific operations with deny-by-default behavior.
- Implementation complexity: Medium.
- Performance tradeoff: policy evaluation complexity.
- Residual risk: scope taxonomy drift across teams.

## Recommended Sequence

1. Immediate

- Reject ID tokens on API endpoints.
- Enforce exact audience checks per route class.
- Emit token-intent mismatch telemetry.

2. Medium-term

- Standardize validation middleware across all services.
- Add issuer/audience/token-use contract tests in CI.

3. Long-term

- Periodically review trust graph across clients, audiences, and scopes.
- Add chaos tests for token replay and policy-drift scenarios.

## When Not to Use a Pattern

- Do not use shared audiences for unrelated critical services where replay risk is high.
- Do not centralize validation without ownership for continuous contract enforcement.
- Do not over-fragment scopes without governance; it can produce policy sprawl and drift.

## Verification Plan

- Replay ID tokens against API endpoints and confirm deterministic rejection.
- Replay audience-B token on audience-A endpoint and confirm rejection.
- Fuzz missing/extra claims and validate consistent deny behavior.
- Run cross-service scope consistency tests for sensitive operations.
