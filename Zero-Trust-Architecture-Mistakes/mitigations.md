# Mitigations - Zero Trust Architecture Mistakes

## Goals

- Remove implicit internal trust paths.
- Enforce strong workload and user identity at each access hop.
- Continuously validate and minimize granted privilege over time.

## Strategy Comparison

| Strategy | Latency Impact | Complexity | Runtime Assurance Gain | Scalability |
| --- | --- | --- | --- | --- |
| Workload identity + mTLS | Medium | High | High | Medium-High |
| Policy parity across enforcement points | Medium | Medium-High | High | Medium |
| Continuous access evaluation | Medium-High | High | Medium-High | Medium |
| Exception lifecycle governance | Low-Medium | Medium | Medium-High | High |
| Hybrid (all above) | Medium-High | High | Very High | Medium |

## Pattern Options

1. Workload identity and mTLS where risk justifies

- Design summary: verify service-to-service identity cryptographically and enforce principal-scoped policies.
- Implementation complexity: High.
- Performance tradeoff: certificate lifecycle and policy distribution overhead.
- Residual risk: partial adoption leaves legacy trust gaps.

2. Policy decision and enforcement parity

- Design summary: ensure policy definitions and runtime enforcement semantics match at each hop.
- Implementation complexity: Medium-High.
- Performance tradeoff: integration and governance overhead.
- Residual risk: version drift under rapid platform changes.

3. Continuous access evaluation

- Design summary: re-evaluate trust as posture/risk context changes, not only at initial auth.
- Implementation complexity: High.
- Performance tradeoff: telemetry and control-plane cost.
- Residual risk: noisy signals if risk models are poorly tuned.

4. Exception lifecycle governance

- Design summary: time-bound exceptions with owners, approvals, and auto-expiry.
- Implementation complexity: Medium.
- Performance tradeoff: process overhead.
- Residual risk: emergency bypass pressure and owner drift.

## Recommended Sequence

1. Immediate

- Inventory and remove broad implicit-trust paths.
- Enforce identity checks on sensitive east-west routes.
- Review and expire stale exceptions.

2. Medium-term

- Roll out workload identity/mTLS in high-risk domains.
- Connect telemetry to policy-drift and exception dashboards.

3. Long-term

- Implement continuous verification model across user/workload/data planes.
- Run recurring adversarial simulations for lateral-movement resistance.

## When Not to Use a Pattern

- Do not enforce strict mTLS globally without migration path for fragile legacy services.
- Do not centralize policy decisions without local fail behavior design.
- Do not scale continuous-risk controls without alert tuning and ownership.

## Verification Plan

- Simulate compromised internal workload and test lateral movement constraints.
- Validate deny-by-default for unauthorized service principals.
- Measure policy drift between intended and observed enforcement behavior.
- Test exception expiry automation and stale-rule rejection paths.
