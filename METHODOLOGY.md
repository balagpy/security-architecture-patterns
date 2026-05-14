# Methodology

Every case study in this repository follows a consistent architecture-analysis workflow.

## Analysis Sequence

1. Define architecture scope and trust boundaries.
2. Document normal identity, request, and control flows.
3. Identify assumptions that can fail under scale or partial outage.
4. Model abuse paths and attacker preconditions.
5. Quantify impact and blast radius.
6. Propose mitigation patterns with explicit tradeoffs.
7. Validate claims with references and, where practical, runnable demos.

## Quality Bar

- Realistic architecture context, not toy-only examples.
- Explicit trust-boundary mapping.
- Failure modes tied to concrete distributed-system behavior.
- Mitigations compared by complexity, latency, and residual risk.
- References to standards, vendor docs, incident analyses, or peer-reviewed work.

## Writing Style

- Prioritize architecture reasoning over payload detail.
- Explain constraints and tradeoffs, not only "best practices".
- Keep reproducible demo steps concise and safe by design.
