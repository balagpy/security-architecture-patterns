# Mitigations - API Gateway Trust Boundaries

## Goals

- make header-based identity non-forgeable
- ensure backend only accepts requests from authenticated trusted callers
- eliminate direct bypass paths around policy enforcement

## Pattern Options

1. Network hardening and private service exposure
- design summary: backend services are private-only; ingress strictly via gateway/service mesh.
- implementation complexity: medium
- performance tradeoff: low
- residual risk: infra drift or emergency exposure changes

2. mTLS with workload identity verification
- design summary: backend validates caller identity (SPIFFE/SVID or equivalent) and only trusts designated gateway/workloads.
- implementation complexity: high
- performance tradeoff: certificate lifecycle overhead
- residual risk: misissued identities, weak policy bindings

3. Signed context headers
- design summary: gateway signs selected headers; backend verifies signature freshness and integrity.
- implementation complexity: medium-high
- performance tradeoff: crypto verification cost per request
- residual risk: key management and replay handling

4. Defense-in-depth authorization
- design summary: backend re-checks sensitive authorization decisions; does not rely on edge-only coarse policy.
- implementation complexity: medium
- performance tradeoff: additional policy evaluation cost
- residual risk: duplicated policy logic if centralization is poor

## Recommended Sequence

1. Immediate
- block direct backend exposure
- reject identity headers from untrusted sources
- add source-identity telemetry at backend

2. Medium-term
- enforce mTLS and caller identity allowlists
- introduce signed context headers for high-risk services

3. Long-term
- unify authorization model across gateway and backend
- continuous trust-boundary validation tests in CI/staging

## Verification Plan

- simulate direct backend requests with forged headers
- validate backend rejection without trusted caller identity
- audit route exposure and ingress rules on each release
- run SSRF pivot tests from internal workloads
