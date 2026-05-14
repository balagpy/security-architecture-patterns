# Mitigations - JWT Revocation Failure

## Goals

- minimize post-revocation token acceptance window
- enforce consistent policy across all service instances
- keep latency and availability within operational limits

## Pattern Options

1. Short-lived Access Tokens + Rotating Refresh Tokens
- design summary: keep access token TTL very short (for example 5-10 minutes) and rotate refresh tokens with replay detection.
- implementation complexity: medium
- performance tradeoff: minimal request-path overhead
- residual risk: non-zero replay window until access token expiry

2. Central Token Introspection for High-Risk Endpoints
- design summary: sensitive operations (payments, admin actions, credential updates) require online liveness check.
- implementation complexity: medium-high
- performance tradeoff: added dependency and latency on request path
- residual risk: introspection outage pressure; must define fail policy

3. Event-Driven Revocation Fan-Out
- design summary: publish revocation events to all auth-enforcing services/gateways for near-real-time cache invalidation.
- implementation complexity: high
- performance tradeoff: operational complexity in messaging reliability and ordering
- residual risk: ordering gaps and consumer lag if not measured

4. Versioned Session State
- design summary: include session/version claim and reject tokens with stale version compared to central session state.
- implementation complexity: medium
- performance tradeoff: requires low-latency state lookup or cache strategy
- residual risk: lookup outages and eventual consistency pitfalls

## Recommended Sequence

1. Immediate
- shorten access token TTL
- enforce denylist checks on highest-risk routes
- instrument revocation latency metrics

2. Medium-term
- implement event-driven invalidation and consistency checks across instances
- remove mixed enforcement paths during deploys

3. Long-term
- standardize identity control plane with explicit SLOs for revocation convergence
- threat-model revocation behavior in architecture reviews

## Verification Plan

- test same revoked token against every replica and gateway hop
- chaos test revocation backend latency/outage and validate policy behavior
- measure: revoke timestamp to final reject timestamp (p95/p99)
- verify no route bypasses centralized policy for sensitive actions
