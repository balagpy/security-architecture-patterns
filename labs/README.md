# security-architecture-labs

Companion practical labs for `security-architecture-patterns`.

## Purpose

This repository provides runnable demonstrations of architecture-level security failures and corresponding mitigation behavior.

## Lab Portfolio

1. `jwt-revocation-lab`
2. `multi-tenant-isolation-lab`
3. `api-gateway-boundary-lab`
4. `oauth-token-confusion-lab`
5. `cicd-supply-chain-lab`
6. `llm-agent-tool-poisoning-lab`
7. `zero-trust-mistakes-lab`

## Lab Design Principles

- architecture-first scenarios
- vulnerable and mitigated paths in the same lab
- deterministic local execution with Docker Compose
- concise runbooks via `run-demo.sh`

## Quick Start

Run any lab:

```bash
cd <lab-directory>
./run-demo.sh
```

## Notes

If Docker daemon is not running, start Docker first and rerun the demo script.
