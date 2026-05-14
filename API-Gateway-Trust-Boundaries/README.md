# API Gateway Trust Boundary Failures

## Executive Summary


API gateways often become a false sense of security. Teams do authentication and coarse authorization at the edge, then downstream services quietly trust forwarded identity headers as if they were cryptographic truth. If a backend is exposed directly, or an internal workload can reach it unexpectedly, that trust collapses fast.

In practice, this is less a single bug and more an architectural boundary mismatch between edge controls and service-level enforcement.

## System Context

Typical system architecture:
- API gateway performs authentication and coarse authorization
- gateway forwards identity context (`X-User-Id`, `X-Role`, `X-Tenant-Id`)
- backend services trust forwarded headers
- internal network assumes gateway-only ingress

Hidden assumption:
- "only trusted gateway can reach service endpoints"

## Baseline Architecture

See `architecture.svg` (rendered) and `diagrams/architecture.mmd` (source).

![Architecture Diagram](./architecture.svg)

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

See `sequence.svg` (rendered) and `diagrams/sequence.mmd` (source).

![Attack Flow Diagram](./attack-flow.svg)

![Sequence Diagram](./sequence.svg)

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

## Why Existing Systems Fail


Most teams do not choose this design out of negligence. They usually inherit it from delivery realities:

- Re-implementing full auth logic in every backend feels expensive and duplicative.
- Temporary internal exposure for debugging or migration often outlives its original purpose.
- Service teams and platform teams ship at different speeds, so boundary controls drift.
- Header-based identity propagation is operationally convenient, so it survives longer than it should.

Over time, "gateway-enforced" becomes an assumption rather than a verified property.

## Real Incident Correlation


This pattern shows up in incidents where internal reachability and caller trust were overestimated:

- Backend endpoints unintentionally reachable from broader network segments.
- Header spoofing or confused-deputy behavior in service-to-service paths.
- SSRF pivots that bypass perimeter checks and land on trusted internal APIs.

The recurring lesson is simple: perimeter controls reduce exposure, but they do not replace caller-authenticity checks at each hop.

## Evidence

Signals to collect for validation:

- Metrics: `time-to-final-reject`, `policy-deny-rate`, and cross-replica decision divergence.
- Logs: identity context, enforcement path, and reason code for allow/deny decisions.
- Tests: replay, propagation-delay, and failover behavior under sustained load.

## Practical Demo

Companion demo:

- [api-gateway-boundary-lab](../demo/api-gateway-boundary-lab/README.md)
- [Run script](../demo/api-gateway-boundary-lab/run-demo.sh)


## Known Limitations


- The demo intentionally simplifies network policy and service-mesh identity controls.
- Real environments often include mixed legacy and modern trust paths not modeled here.
- Mitigations reduce spoofing risk but still require strong key/cert lifecycle operations.

## References

See [references.md](./references.md).
