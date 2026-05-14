# Zero Trust Architecture Mistakes in Real Deployments

## Executive Summary

Many "zero trust" programs fail by implementing identity checks at the edge while preserving implicit trust inside networks, workloads, and service paths. The mismatch between policy intent and runtime enforcement creates false assurance.

This is a governance-to-runtime architecture gap, not a branding issue.

## System Context

Common enterprise shape:
- SSO and MFA at user ingress
- segmented networks with partial microsegmentation
- mixed legacy and cloud-native workloads
- service-to-service traffic with uneven identity enforcement

Zero trust invariant:
- every access decision should be continuously verified with strong identity, context, and policy

## Baseline Architecture

See `architecture.svg` (rendered) and `diagrams/architecture.mmd` (source).

## Normal Flow

1. User/workload authenticates.
2. Policy engine evaluates access context.
3. Access granted with least privilege.
4. Continuous signals can revoke/adjust trust.

## Failure Modes

1. Perimeter-only verification
- strong user login controls, weak internal service auth

2. Flat east-west trust
- workloads on same segment can communicate broadly by default

3. Static long-lived credentials
- no continuous verification or context-based re-evaluation

4. Policy bypass exceptions
- urgent allowlist exceptions become permanent hidden backdoors

## Attack/Abuse Flow

See `attack-flow.svg` (rendered) and `diagrams/attack-flow.mmd` (source).

## Impact

- Confidentiality: lateral movement after initial foothold.
- Integrity: unauthorized internal operations.
- Availability: broad blast radius in ransomware-style propagation.
- Governance: compliance posture appears stronger than actual runtime enforcement.

## Detection Opportunities

- high-volume east-west connections outside baseline policy intent
- service calls lacking workload identity proofs
- stale privileged exceptions and unused allow rules
- mismatch between policy definition and observed enforcement

## Mitigation Strategy

See [mitigations.md](./mitigations.md).

## Practical Demo

Companion lab:
- [zero-trust-mistakes-lab](../demo/zero-trust-mistakes-lab/README.md)

## References

See [references.md](./references.md).
