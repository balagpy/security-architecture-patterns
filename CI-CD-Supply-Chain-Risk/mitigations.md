# Mitigations - CI/CD Supply Chain Risk

## Goals

- reduce trust in mutable external build inputs
- enforce provenance and integrity from source to deploy
- limit blast radius of runner compromise

## Pattern Options

1. Pin actions and dependencies immutably
- design summary: use commit SHA pinning for CI actions and deterministic lockfiles for dependencies.
- implementation complexity: low-medium
- performance tradeoff: minimal
- residual risk: pinned artifact itself may be malicious if pin was not vetted

2. Least-privilege workflow permissions
- design summary: per-workflow and per-job scoped tokens, no broad write/admin defaults.
- implementation complexity: medium
- performance tradeoff: operational tuning overhead
- residual risk: privilege creep over time without periodic audit

3. Isolated and ephemeral runners
- design summary: short-lived clean runners with restricted egress and strong secret controls.
- implementation complexity: high
- performance tradeoff: infra cost and startup latency
- residual risk: runtime exploit within job window

4. Artifact signing and provenance verification
- design summary: sign artifacts and verify signatures/provenance before promotion/deploy.
- implementation complexity: medium-high
- performance tradeoff: added verification steps
- residual risk: key management weaknesses

## Recommended Sequence

1. Immediate
- pin mutable references
- reduce token permissions
- block secret exposure to untrusted contexts

2. Medium-term
- enforce provenance checks at deploy gates
- introduce policy checks for workflow changes

3. Long-term
- full SLSA-aligned controls with attestation and continuous compliance checks

## Verification Plan

- simulate mutable action tag drift and ensure policy blocks
- attempt deploy with unsigned artifact and confirm rejection
- run red-team style CI permission abuse scenarios in staging
