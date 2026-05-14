# Mitigations - Multi-Tenant SaaS Isolation

## Goals

- make tenant boundary non-bypassable by default
- remove developer-dependent manual scoping patterns
- ensure uniform policy across API, workers, cache, and data planes

## Pattern Options

1. Database-enforced tenant isolation
- design summary: enforce row-level security (RLS) or equivalent policies keyed to authenticated tenant context.
- implementation complexity: medium-high
- performance tradeoff: policy planning overhead, indexing requirements
- residual risk: policy misconfiguration and privileged bypass roles

2. Typed tenant context propagation
- design summary: tenant identity propagated via signed internal identity or service token claims, not mutable headers.
- implementation complexity: medium
- performance tradeoff: minimal
- residual risk: legacy services with mixed trust assumptions

3. Mandatory query guards in data access layer
- design summary: shared repository/ORM wrappers require tenant scope for all entity operations.
- implementation complexity: medium
- performance tradeoff: low
- residual risk: raw SQL escape hatches and migration scripts

4. Tenant-scoped cache and queue namespaces
- design summary: namespace all cache keys and async job payloads by tenant and auth context version.
- implementation complexity: low-medium
- performance tradeoff: larger keyspace and metadata overhead
- residual risk: old keys/jobs lingering after schema changes

## Recommended Sequence

1. Immediate
- block known unscoped endpoints
- enforce cache key namespacing standards
- add runtime guards for missing tenant scope

2. Medium-term
- centralize authorization and tenant context libraries
- adopt tenant policy tests in CI

3. Long-term
- database-level policy enforcement
- continuous isolation verification and attack simulation

## Verification Plan

- contract tests asserting all list/get/update/delete paths require tenant scope
- synthetic cross-tenant probes in staging
- log correlation: token tenant vs data tenant on sampled requests
- chaos tests for worker/context reuse under concurrency
