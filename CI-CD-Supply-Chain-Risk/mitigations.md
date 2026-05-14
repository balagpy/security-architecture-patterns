# Mitigations - CI/CD Supply Chain Risk

## Goals

- Reduce trust in mutable external build inputs.
- Enforce source-to-deploy provenance and integrity.
- Limit blast radius of runner or pipeline compromise.

## Strategy Comparison

| Strategy | Latency Impact | Complexity | Integrity Assurance Gain | Scalability |
| --- | --- | --- | --- | --- |
| Immutable action/dependency pinning | Low | Medium | High | High |
| Least-privilege workflow permissions | Low | Medium | High | High |
| Ephemeral runner hardening | Medium | High | Medium-High | Medium |
| Artifact signing + verification gate | Medium | Medium-High | High | Medium-High |
| Hybrid (all above) | Medium | High | Very High | Medium-High |

## Pattern Options

1. Pin actions and dependencies immutably

- Design summary: use commit SHA pinning for actions and deterministic lockfiles for dependencies.
- Implementation complexity: Medium.
- Performance tradeoff: minimal runtime overhead, moderate maintenance discipline.
- Residual risk: trusted pin can still be wrong if review process is weak.

2. Least-privilege workflow permissions

- Design summary: per-workflow and per-job scoped tokens, no broad write/admin defaults.
- Implementation complexity: Medium.
- Performance tradeoff: low runtime cost, moderate policy governance overhead.
- Residual risk: permission sprawl over time without regular audits.

3. Isolated and ephemeral runners

- Design summary: short-lived clean runners with restricted egress and hardened execution context.
- Implementation complexity: High.
- Performance tradeoff: infra cost and startup latency.
- Residual risk: exploit still possible inside job window if controls are incomplete.

4. Artifact signing and provenance verification

- Design summary: sign artifacts and enforce signature/attestation verification before deploy.
- Implementation complexity: Medium-High.
- Performance tradeoff: added deploy gate checks and key management burden.
- Residual risk: verification bypass through emergency/manual channels.

## Recommended Sequence

1. Immediate

- Pin mutable references.
- Tighten workflow permission scopes.
- Block secret exposure to untrusted execution contexts.

2. Medium-term

- Enforce deploy-time provenance checks.
- Add policy checks for workflow-file changes and privileged job paths.

3. Long-term

- Align controls to SLSA/SSDF maturity targets.
- Run recurring adversarial pipeline simulations.

## When Not to Use a Pattern

- Do not over-constrain workflows without staged migration, or teams may bypass controls operationally.
- Do not treat signing as complete if provenance verification is optional.
- Do not rely on static long-lived self-hosted runners for privileged release paths.

## Verification Plan

- Simulate mutable action-tag drift and ensure policy blocks execution.
- Attempt deploy with unsigned artifact and confirm deterministic rejection.
- Run token-permission abuse scenarios in staging pipelines.
- Audit runner egress and secret-use patterns for unexpected destinations.
