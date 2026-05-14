# Security Review Checklist

Use this checklist during architecture reviews and pre-release security design assessments.

## Identity and Session State

- Are identity assertions verified at every enforcement hop?
- Can session/token state become stale between control and data planes?
- Is revocation convergence measured with explicit SLOs?

## Trust Boundaries

- Are trust boundaries documented and enforced in runtime policy?
- Can mutable headers or metadata bypass caller-identity guarantees?
- Are internal paths protected against direct/bypass access?

## Multi-Tenant and Data Isolation

- Is tenant context mandatory in all read/write paths?
- Are cache keys and job payloads tenant-scoped?
- Are cross-tenant access probes part of testing strategy?

## Control Plane and Supply Chain

- Are CI/CD actions and dependencies pinned immutably?
- Are artifact provenance/signature checks enforced before deploy?
- Are pipeline credentials least-privilege and context-scoped?

## Agentic / Emerging Architectures

- Can untrusted retrieved content trigger high-risk tool execution?
- Is there an explicit intent-to-tool allowlist policy?
- Are high-risk actions gated by confirmation and audit trails?

## Detection and Response

- Are key detection signals defined for each failure mode?
- Can incident responders trace decision provenance across services?
- Are known fail-open controls documented with bounded blast radius?
