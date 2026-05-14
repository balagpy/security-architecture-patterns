# Mitigations - Multi-Tenant SaaS Isolation

## Goals

- Make tenant boundary non-bypassable by default.
- Remove manual, developer-dependent scoping patterns.
- Enforce uniform policy across API, worker, cache, and data planes.

## Strategy Comparison

| Strategy | Latency Impact | Complexity | Isolation Assurance Gain | Scalability |
| --- | --- | --- | --- | --- |
| Tenant-scoped DAL guards | Low | Medium | High | High |
| Cache + queue namespacing | Low | Low-Medium | Medium-High | High |
| Data-layer RLS enforcement | Medium | Medium-High | High | Medium-High |
| Signed tenant context propagation | Low-Medium | Medium | Medium-High | High |
| Hybrid (all above) | Medium | High | Very High | Medium-High |

## Pattern Options

1. Database-enforced tenant isolation

- Design summary: enforce row-level security (RLS) or equivalent policy keyed to authenticated tenant context.
- Implementation complexity: Medium-High.
- Performance tradeoff: query planning overhead and role model complexity.
- Residual risk: policy misconfiguration or privileged bypass roles.

2. Typed tenant context propagation

- Design summary: tenant identity propagated through signed/internal identity context, not mutable client headers.
- Implementation complexity: Medium.
- Performance tradeoff: minimal runtime overhead.
- Residual risk: legacy paths still accepting weak context contracts.

3. Mandatory query guards in data access layer

- Design summary: shared DAL/repository wrappers require tenant scope for all entity operations.
- Implementation complexity: Medium.
- Performance tradeoff: low request-path overhead.
- Residual risk: raw SQL escape paths and migration tooling bypass.

4. Tenant-scoped cache and queue namespaces

- Design summary: namespace all cache keys and async payloads by tenant and context version.
- Implementation complexity: Low-Medium.
- Performance tradeoff: larger keyspace and metadata overhead.
- Residual risk: stale keys/jobs and partial adoption across services.

## Recommended Sequence

1. Immediate

- Block known unscoped endpoint/query paths.
- Enforce tenant-namespaced cache standards.
- Add runtime guards for missing tenant context.

2. Medium-term

- Centralize tenant-context and authorization libraries.
- Introduce tenant-isolation contract tests in CI.

3. Long-term

- Add data-layer policy enforcement (RLS or equivalent).
- Run continuous isolation simulations and adversarial probes.

## When Not to Use a Pattern

- Do not rely only on cache namespacing without query-level tenant enforcement.
- Do not enforce RLS without clear database role and migration strategy.
- Do not over-index on centralized policy if service owners cannot operate context contracts consistently.

## Verification Plan

- Contract tests for tenant scope on all read/write operations.
- Synthetic cross-tenant probes in staging and pre-production.
- Query log validation for mandatory tenant predicates.
- Async worker chaos tests for context leakage and replay.
