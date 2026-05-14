# Mitigations - OAuth Token Confusion

## Goals

- enforce strict token intent per endpoint
- bind each resource server to explicit issuer and audience policy
- remove ambiguous acceptance paths in auth middleware

## Pattern Options

1. Strict token profile validation
- design summary: validate `iss`, `aud`, expiry, token type/usage, and required claims before authorization.
- implementation complexity: medium
- performance tradeoff: low
- residual risk: policy drift between services

2. Per-resource-server audience isolation
- design summary: each API has unique audience and rejects foreign tokens.
- implementation complexity: medium
- performance tradeoff: low
- residual risk: migration complexity in large estates

3. Centralized auth middleware with contract tests
- design summary: shared validation library and mandatory endpoint-level policy tests.
- implementation complexity: medium-high
- performance tradeoff: minimal runtime overhead
- residual risk: bypass via legacy/custom handlers

4. Scope and action binding
- design summary: map required scopes/claims to operation-level policy with deny-by-default.
- implementation complexity: medium
- performance tradeoff: policy evaluation overhead
- residual risk: mis-scoped tokens from IdP config errors

## Recommended Sequence

1. Immediate
- reject ID tokens on API endpoints
- enforce exact audience checks
- instrument token-intent mismatch metrics

2. Medium-term
- standardize validation middleware across all services
- add issuer/audience/scope policy contract tests

3. Long-term
- periodic trust-graph review across clients, audiences, scopes, and issuers
- continuous chaos tests for token misuse scenarios

## Verification Plan

- replay ID token against API endpoints and confirm rejection
- replay token from audience B to audience A and confirm rejection
- fuzz missing/extra claims and validate deterministic deny behavior
