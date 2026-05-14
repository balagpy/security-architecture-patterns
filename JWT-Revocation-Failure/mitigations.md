# Mitigations - JWT Revocation Failure

## Goals

- Minimize post-revocation token acceptance window.
- Enforce consistent policy across service replicas.
- Keep latency and availability within explicit operational limits.

## Strategy Comparison

| Strategy | Latency Impact | Complexity | Revocation Speed | Scalability |
| --- | --- | --- | --- | --- |
| Local cache denylist only | Low | Medium | Medium-Low | High |
| Per-request token introspection | High | Medium | High | Medium-Low |
| Short-lived access tokens only | Very low | Low | Low-Medium | High |
| Event-driven invalidation + cache | Low-Medium | High | High | High |
| Hybrid: cache + selective introspection | Medium | High | High | Medium-High |

## Pattern Options

1. Short-lived access tokens + rotating refresh tokens

- Design summary: reduce access-token lifetime and rotate refresh tokens with replay detection.
- Implementation complexity: Medium.
- Performance tradeoff: low request-path overhead, higher token refresh volume.
- Residual risk: replay window still exists until access-token expiry.

2. Central token introspection for high-risk endpoints

- Design summary: require online liveness checks for sensitive operations.
- Implementation complexity: Medium-High.
- Performance tradeoff: additional dependency and latency in request path.
- Residual risk: introspection outages require strict fail policy choices.

3. Event-driven revocation fan-out

- Design summary: publish revocation events and invalidate local caches quickly across all instances.
- Implementation complexity: High.
- Performance tradeoff: messaging reliability and ordering overhead.
- Residual risk: consumer lag, replay window if delivery is delayed.

4. Versioned session state

- Design summary: embed session version in token and reject stale versions against central state.
- Implementation complexity: Medium.
- Performance tradeoff: central state lookup or synchronized cache requirement.
- Residual risk: consistency and availability pressure on state service.

## Recommended Sequence

1. Immediate

- Shorten access-token TTL.
- Enforce denylist checks on highest-risk routes.
- Instrument revocation convergence metrics.

2. Medium-term

- Add event-driven invalidation and consistency checks.
- Eliminate mixed enforcement behavior during rollout.

3. Long-term

- Define revocation convergence SLOs at platform level.
- Add revocation behavior to architecture review gates.

## Verification Plan

- Replay a revoked token against every replica and route class.
- Inject revocation-backend latency/outage and verify deterministic behavior.
- Measure revoke-event timestamp to final-reject timestamp (`p95`, `p99`).
- Validate no high-risk route bypasses liveness enforcement.
