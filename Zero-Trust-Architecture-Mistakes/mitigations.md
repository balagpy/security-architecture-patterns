# Mitigations - Zero Trust Architecture Mistakes

## Goals

- remove implicit internal trust paths
- enforce strong workload and user identity on every access path
- continuously validate and minimize granted privileges

## Pattern Options

1. Workload identity and mTLS everywhere practical
- design summary: authenticate service-to-service calls with verifiable workload identity.
- implementation complexity: high
- performance tradeoff: cert lifecycle and control-plane overhead
- residual risk: policy gaps in legacy systems

2. Policy decision and enforcement parity
- design summary: ensure defined policies are consistently enforced at each hop.
- implementation complexity: medium-high
- performance tradeoff: integration effort
- residual risk: drift during rapid platform changes

3. Continuous access evaluation
- design summary: re-evaluate trust on context changes (device posture, behavior, risk signals).
- implementation complexity: high
- performance tradeoff: control-plane and telemetry costs
- residual risk: noisy signals and false positives

4. Exception lifecycle governance
- design summary: time-bound exceptions with owners, review cadence, and automatic expiry.
- implementation complexity: medium
- performance tradeoff: operational process overhead
- residual risk: emergency bypass pressure

## Recommended Sequence

1. Immediate
- inventory and remove broad implicit-trust paths
- enforce identity checks on sensitive east-west routes
- review and expire stale policy exceptions

2. Medium-term
- roll out workload identity and mTLS in priority domains
- connect telemetry to policy validation dashboards

3. Long-term
- full continuous verification model across user, workload, and data planes
- regular adversarial simulations for lateral movement resistance

## Verification Plan

- simulate compromised internal workload and test movement constraints
- verify deny-by-default on unauthorized service calls
- measure policy drift between intended and observed runtime behavior
