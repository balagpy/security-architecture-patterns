# OAuth Token Confusion in Distributed Services

## Executive Summary

OAuth token confusion happens when services accept token types, audiences, or issuers beyond what the endpoint is designed to trust. Common examples include using ID tokens as API access tokens, accepting access tokens minted for a different audience, or failing to bind token validation to resource-server-specific expectations.

This is a protocol-usage architecture failure, not just a parsing bug.

## System Context

Typical system:
- identity provider issues ID token and access token
- API gateway or backend validates JWT structure/signature
- multiple resource servers exist with different audiences/scopes

Expected invariant:
- each endpoint accepts only the token type and audience explicitly intended for it

## Baseline Architecture

See `architecture.svg` (rendered) and `diagrams/architecture.mmd` (source).

## Normal Flow

1. Client receives ID token (for client authentication context) and access token (for API access).
2. Client calls API with access token.
3. API verifies signature, issuer, audience, expiry, and scopes.
4. API authorizes operation based on claims and policy.

## Failure Modes

1. ID token accepted as access token
- backend checks signature/expiry only
- ignores token type (`typ`) and intended use

2. Audience confusion
- service accepts token with `aud=service-b` at `service-a`
- cross-service replay becomes possible

3. Weak issuer/tenant checks
- token from different issuer/tenant accepted due to broad JWKS trust

4. Scope and subject confusion
- token has valid identity but insufficient scope; endpoint authorizes anyway

## Attack/Abuse Flow

See `attack-flow.svg` (rendered) and `diagrams/attack-flow.mmd` (source).

## Impact

- Confidentiality: unauthorized data access via replayed/misused tokens.
- Integrity: actions performed with wrong trust context.
- Lateral movement: token replay between services with overlapping trust assumptions.
- Audit ambiguity: valid signatures hide invalid token intent.

## Detection Opportunities

- token usage where `aud` does not match target service
- ID-token-like claims observed on API authorization paths
- high rate of denied/accepted mismatches on scope checks
- issuer variance anomalies per endpoint

## Mitigation Strategy

See [mitigations.md](./mitigations.md).

## Practical Demo

Companion lab:
- [oauth-token-confusion-lab](../demo/oauth-token-confusion-lab/README.md)

## References

See [references.md](./references.md).
