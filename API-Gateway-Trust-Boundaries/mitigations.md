# Mitigations - API Gateway Trust Boundaries

## Goals

- Make identity context non-forgeable at every enforcement hop.
- Ensure backend services accept traffic only from authenticated trusted callers.
- Eliminate direct bypass paths around edge policy enforcement.

## Strategy Comparison

| Strategy | Latency Impact | Complexity | Boundary Integrity Gain | Scalability |
| --- | --- | --- | --- | --- |
| Private backend ingress only | Low | Medium | High | High |
| mTLS workload identity | Low-Medium | High | High | Medium-High |
| Signed header context | Medium | Medium-High | Medium-High | High |
| Backend re-authorization | Medium | Medium | High | Medium |
| Hybrid: mTLS + signed context + backend check | Medium | High | Very High | Medium-High |

## Pattern Options

1. Network hardening and private service exposure

- Design summary: backend services are private-only; ingress strictly through gateway/mesh paths.
- Implementation complexity: Medium.
- Performance tradeoff: minimal request-path overhead.
- Residual risk: emergency exposure changes and policy drift.

2. mTLS with workload identity verification

- Design summary: backend validates caller workload identity and only trusts designated gateway/workloads.
- Implementation complexity: High.
- Performance tradeoff: cert lifecycle and identity policy overhead.
- Residual risk: misissued identity or weak principal scoping.

3. Signed context headers

- Design summary: gateway signs identity headers; backend verifies signature, timestamp freshness, and key trust.
- Implementation complexity: Medium-High.
- Performance tradeoff: cryptographic verification cost per request.
- Residual risk: key rotation gaps, replay handling mistakes.

4. Defense-in-depth authorization

- Design summary: backend re-checks high-risk authorization decisions, not only edge-level policy.
- Implementation complexity: Medium.
- Performance tradeoff: additional policy evaluation latency.
- Residual risk: policy duplication and divergence if governance is weak.

## Recommended Sequence

1. Immediate

- Remove direct backend exposure.
- Reject identity headers from untrusted callers.
- Add caller-identity telemetry to backend allow/deny paths.

2. Medium-term

- Enforce mTLS with strict caller principal allowlists.
- Add signed header context validation for sensitive routes.

3. Long-term

- Unify authorization semantics across gateway and backend policy engines.
- Add continuous trust-boundary regression tests in CI/staging.

## When Not to Use a Pattern

- Do not rely on signed headers as primary control when backend reachability is still broad.
- Do not rely on mTLS alone for user-role authorization correctness.
- Do not apply synchronous central auth checks on every low-risk route without throughput modeling.

## Verification Plan

- Simulate direct backend access with forged identity headers.
- Verify hard reject without trusted caller identity.
- Run SSRF pivot simulations from internal workloads.
- Audit ingress/service-exposure policy on every release.
