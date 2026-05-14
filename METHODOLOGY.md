# Methodology

Every case study follows this sequence:

1. Define the architecture scope and trust boundaries.
2. Document normal request and identity flows.
3. Identify design assumptions that break at scale.
4. Model attacker paths and abuse preconditions.
5. Quantify impact and blast radius.
6. Propose mitigation patterns with tradeoffs.
7. Validate claims with references and, where practical, lab simulation.

## Quality Bar

- Realistic architecture context (not toy examples)
- Explicit trust-boundary analysis
- Failure modes tied to concrete distributed-system behavior
- Mitigation options compared by complexity, latency, and risk reduction
- References to standards, vendor docs, papers, or incident writeups

## Style Rules

- Prefer architecture reasoning over payload detail
- Explain constraints and tradeoffs, not only "best practices"
- Keep reproducible lab steps minimal and safe by design
