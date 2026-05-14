# API Gateway Trust Boundary Failures

## Executive Summary

API gateways are often assumed to be a hard trust boundary, but downstream services frequently accept identity and authorization headers without verifying call provenance. If internal services are reachable directly, or if network/policy controls are weak, attackers can bypass the gateway and inject privileged headers.

This is not only an auth bug. It is a boundary-design failure between edge, mesh, and service layers.

## System Context

Typical system:
- API gateway performs authentication and coarse authorization
- gateway forwards identity context (`X-User-Id`, `X-Role`, `X-Tenant-Id`)
- backend services trust forwarded headers
- internal network assumes gateway-only ingress

Hidden assumption:
- "only trusted gateway can reach service endpoints"

## Baseline Architecture

See `architecture.svg` (rendered) and `diagrams/architecture.mmd` (source).

## Normal Flow

1. Client authenticates at gateway.
2. Gateway validates token and policy.
3. Gateway injects trusted identity headers.
4. Backend processes request using those headers.

## Failure Modes

1. Direct backend reachability
- service exposed via misconfigured load balancer, ingress, or service port
- attacker calls backend directly and sends forged identity headers

2. Header trust without authenticity
- backend treats plain headers as truth
- no signature, mTLS identity binding, or provenance checks

3. Policy drift between gateway and backend
- gateway enforces new rules, backend has legacy allow-paths
- bypass path remains exploitable

4. Internal SSRF pivot
- compromised internal service can call sensitive backend and set privileged headers

## Attack/Abuse Flow

See `attack-flow.svg` (rendered) and `diagrams/attack-flow.mmd` (source).

## Impact

- Confidentiality: unauthorized access to tenant/user data.
- Integrity: privileged actions via forged admin/service roles.
- Availability: bypass can hit internal endpoints not rate-limited at edge.
- Governance: false confidence in "gateway secured everything" posture.

## Detection Opportunities

- requests containing identity headers from non-gateway sources
- backend traffic that lacks expected mTLS client identity
- backend request rates from unexpected source CIDRs/workloads
- divergence between gateway decision logs and backend action logs

## Mitigation Strategy

See [mitigations.md](./mitigations.md).

## Practical Demo

Companion lab:
- [api-gateway-boundary-lab](../labs/api-gateway-boundary-lab/README.md)

## References

See [references.md](./references.md).
