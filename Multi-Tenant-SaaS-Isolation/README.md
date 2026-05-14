# Multi-Tenant SaaS Isolation Failures

## Executive Summary


Multi-tenant isolation usually fails in small, boring places rather than dramatic exploits: one missing tenant predicate, one cache key without namespace, one background worker that reuses stale context. Those small misses can produce full cross-tenant exposure.

The core issue is boundary enforcement consistency across API, cache, queue, and data layers.

## System Context

Typical architecture:
- shared API and worker tiers
- shared database with row-level tenant segregation
- shared cache and queue infrastructure
- tenant context passed via JWT claims and request headers

Security invariant:
- every read/write must be constrained by authenticated tenant identity

## Baseline Architecture

See `architecture.svg` (rendered) and `diagrams/architecture.mmd` (source).

![Architecture Diagram](./architecture.svg)

## Normal Flow

1. User authenticates and receives token with `tenant_id`.
2. API extracts tenant context and authorization scope.
3. Query/data access layer enforces tenant filter.
4. Cache keys include tenant namespace.
5. Response returns tenant-scoped data only.

## Failure Modes

1. Missing tenant predicate in one code path
- an endpoint uses `resource_id` without `tenant_id` filter
- attacker iterates predictable IDs to access foreign tenant records

2. Cache namespace collision
- key is `invoice:{id}` instead of `tenant:{tenant_id}:invoice:{id}`
- tenant A receives tenant B data from cache

3. Internal service trust confusion
- downstream service trusts forwarded `X-Tenant-ID` header without verifying caller/service identity

4. Background job context leakage
- queue consumer reuses stale execution context and applies wrong tenant scope

## Attack/Abuse Flow

See `attack-flow.svg` (rendered) and `diagrams/attack-flow.mmd` (source).

See `sequence.svg` (rendered) and `diagrams/sequence.mmd` (source).

![Attack Flow Diagram](./attack-flow.svg)

![Sequence Diagram](./sequence.svg)

## Impact

- Confidentiality: cross-tenant data leakage.
- Integrity: cross-tenant updates/deletes.
- Compliance: contractual and regulatory breach.
- Business: severe trust and platform reputation damage.

## Detection Opportunities

- queries returning records where `token.tenant_id != row.tenant_id`
- cache hit anomalies across tenant namespaces
- tenant-switch patterns from same principal/device within short windows
- shadow authorization logs for denied cross-tenant attempts

## Mitigation Strategy

See [mitigations.md](./mitigations.md).

## Why Existing Systems Fail


Teams generally make rational tradeoffs that create isolation debt:

- Shared infrastructure is economically necessary early on.
- Throughput work (caching, async processing) lands before authorization abstractions are mature.
- Legacy interfaces keep mutable tenant context in headers for compatibility.
- One weak path can bypass several strong ones.

Isolation is only as strong as the least-enforced data path.

## Real Incident Correlation


Industry incidents repeatedly map to this class of failure:

- Cross-tenant leakage from cache namespace collisions.
- Access-control drift where one query path omitted tenant scoping.
- IAM and policy misconfiguration exposing data between tenants.

These are usually systems-integration failures, not one-off coding mistakes.

## Evidence

Signals to collect for validation:

- Metrics: `time-to-final-reject`, `policy-deny-rate`, and cross-replica decision divergence.
- Logs: identity context, enforcement path, and reason code for allow/deny decisions.
- Tests: replay, propagation-delay, and failover behavior under sustained load.

## Practical Demo

Companion demo:

- [multi-tenant-isolation-lab](../demo/multi-tenant-isolation-lab/README.md)
- [Run script](../demo/multi-tenant-isolation-lab/run-demo.sh)


## Known Limitations


- The demo uses small synthetic datasets and simplified tenancy metadata.
- It does not model full policy engines, legal controls, or customer-specific segmentation.
- Production isolation posture should be validated with data-layer and control-plane tests together.

## References

See [references.md](./references.md).
