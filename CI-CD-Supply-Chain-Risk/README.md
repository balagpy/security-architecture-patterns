# CI/CD Supply Chain Risk in Modern Delivery Pipelines

## Executive Summary


CI/CD systems are trust multipliers: if the pipeline is compromised, downstream releases inherit that compromise quickly. In many organizations, build and release paths have broad privilege because speed matters, and that makes them high-value targets.

The architectural risk is trust transitivity from source to build to artifact to deployment.

## System Context

Typical pipeline:
- source repository and pull request workflow
- CI runner executing workflow definitions
- third-party actions/plugins and package dependencies
- artifact registry and deployment system

Security invariant:
- only reviewed and trusted code should reach production artifacts

## Baseline Architecture

See `architecture.svg` (rendered) and `diagrams/architecture.mmd` (source).

![Architecture Diagram](./architecture.svg)

## Normal Flow

1. Developer opens PR.
2. CI runs tests/build with dependencies and actions.
3. Artifact is built, signed, and pushed.
4. CD deploys approved artifact to environments.

## Failure Modes

1. Unpinned third-party actions
- workflow references mutable tags (`@v1`) instead of commit SHA
- upstream compromise changes runtime behavior silently

2. Dependency confusion/poisoning
- malicious package resolved due to namespace/version ambiguity

3. Secrets exposure in CI context
- overly broad tokens available to untrusted PR contexts

4. Artifact integrity gaps
- deploy stage does not verify provenance/signature

## Attack/Abuse Flow

See `attack-flow.svg` (rendered) and `diagrams/attack-flow.mmd` (source).

See `sequence.svg` (rendered) and `diagrams/sequence.mmd` (source).

![Attack Flow Diagram](./attack-flow.svg)

![Sequence Diagram](./sequence.svg)

## Impact

- Confidentiality: exfiltration of secrets/tokens from runner.
- Integrity: malicious artifact promotion to production.
- Availability: pipeline disruption and rollback instability.
- Trust: release credibility and customer confidence damage.

## Detection Opportunities

- workflow changes that broaden permissions unexpectedly
- action version drift without corresponding review
- unsigned/unverifiable artifacts reaching deployment
- anomalous outbound network patterns during build

## Mitigation Strategy

See [mitigations.md](./mitigations.md).

## Why Existing Systems Fail


Teams usually optimize for delivery throughput first, then retrofit controls:

- Mutable references are easier to maintain than immutable pins.
- Broad tokens reduce operational friction for automation.
- Provenance checks are deferred to keep deployment lead time low.
- Third-party integrations accumulate faster than risk governance.

The result is a powerful control plane with uneven integrity boundaries.

## Real Incident Correlation


This maps cleanly to widely studied supply-chain incidents:

- CircleCI: credential/session exposure impact patterns.
- SolarWinds: build-chain trust compromise at scale.
- Codecov: script-integrity and secret-exposure pathway.

Different mechanics, same architectural lesson: release integrity must be verified, not assumed.

## Evidence

Signals to collect for validation:

- Metrics: `time-to-final-reject`, `policy-deny-rate`, and cross-replica decision divergence.
- Logs: identity context, enforcement path, and reason code for allow/deny decisions.
- Tests: replay, propagation-delay, and failover behavior under sustained load.

## Practical Demo

Companion demo:

- [cicd-supply-chain-lab](../demo/cicd-supply-chain-lab/README.md)
- [Run script](../demo/cicd-supply-chain-lab/run-demo.sh)


## Known Limitations


- The demo models policy decisions rather than a full enterprise build platform.
- It does not emulate every runner-hardening or secret-management control.
- Real resilience requires controls across code review, build, signing, and deploy gates together.

## References

See [references.md](./references.md).
