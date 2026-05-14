# Pattern Index

This index maps architecture failures to reusable security design patterns.

## Identity and Session Consistency

- JWT revocation convergence failures.
- Token liveness vs signature-validity split.
- Stale enforcement windows across replicas.

Case study:
- [JWT Revocation Failure](./JWT-Revocation-Failure/README.md)

## Tenant and Data Boundary Integrity

- Missing tenant scoping in query/cache/job paths.
- Context propagation drift across services.
- Boundary collapse under shared infrastructure.

Case study:
- [Multi-Tenant SaaS Isolation](./Multi-Tenant-SaaS-Isolation/README.md)

## Trust Boundary and Identity Propagation

- Gateway-to-service trust assumptions.
- Forged internal identity headers.
- Direct backend exposure outside policy path.

Case study:
- [API Gateway Trust Boundaries](./API-Gateway-Trust-Boundaries/README.md)

## OAuth and Token Intent Integrity

- ID token vs access token misuse.
- Audience confusion across services.
- Weak issuer/scope/claim enforcement.

Case study:
- [OAuth Token Confusion](./OAuth-Token-Confusion/README.md)

## Software Supply Chain Trust

- Mutable CI action/dependency trust.
- Excessive workflow permissions.
- Missing artifact provenance verification.

Case study:
- [CI/CD Supply Chain Risk](./CI-CD-Supply-Chain-Risk/README.md)

## Agentic AI Tooling Trust

- Prompt/tool poisoning through untrusted retrieval.
- Over-privileged tool execution.
- Missing intent-to-tool policy bindings.

Case study:
- [LLM Agent Tool Poisoning](./LLM-Agent-Tool-Poisoning/README.md)

## Zero Trust Runtime Reality

- Perimeter-heavy, east-west-light enforcement.
- Implicit internal trust paths.
- Stale exceptions and policy-to-runtime drift.

Case study:
- [Zero Trust Architecture Mistakes](./Zero-Trust-Architecture-Mistakes/README.md)

## Operational Design Checklist

Use this checklist during architecture and threat-model reviews.

1. Is identity authenticity checked at every enforcement hop?
2. Are boundary decisions tied to strong caller identity, not mutable headers?
3. Are tenant/session constraints impossible to omit by convention alone?
4. What is the maximum inconsistency window under failure conditions?
5. Can token type and audience confusion be exploited across services?
6. Which CI/CD inputs are mutable and unauthenticated?
7. Can untrusted retrieved content trigger high-risk agent tools?
8. Which east-west paths still rely on implicit trust?
9. Which controls fail open, and what is the blast radius?
