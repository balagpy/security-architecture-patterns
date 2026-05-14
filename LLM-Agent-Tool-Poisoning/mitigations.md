# Mitigations - LLM Agent Tool Poisoning

## Goals

- prevent untrusted content from directly authorizing tool execution
- minimize blast radius of mistaken tool calls
- preserve auditable decision provenance

## Pattern Options

1. Intent-to-tool allowlist policy
- design summary: map user-approved intents to explicit allowed tool categories and blocked operations.
- implementation complexity: medium
- performance tradeoff: low
- residual risk: policy gaps for novel task variants

2. Trust-tiered context separation
- design summary: separate system/user policies from retrieved external content; treat retrieval as data, not instruction.
- implementation complexity: medium
- performance tradeoff: low-medium prompt overhead
- residual risk: model can still misinterpret without strong policy checks

3. Step-up confirmation for high-risk actions
- design summary: require explicit user confirmation for file writes, network egress, privileged commands.
- implementation complexity: low-medium
- performance tradeoff: interaction latency
- residual risk: social engineering if confirmation UX is weak

4. Tool capability sandboxing
- design summary: least-privilege execution, scoped filesystems, egress controls, per-tool tokens.
- implementation complexity: high
- performance tradeoff: infra and operational overhead
- residual risk: sandbox escape or misconfiguration

## Recommended Sequence

1. Immediate
- enforce deny-by-default tool policy
- add step-up confirmation for high-risk actions
- log source-provenance for every tool call

2. Medium-term
- implement trust-tier context segregation
- build continuous tests with adversarial prompt/tool injection cases

3. Long-term
- policy-as-code for agent safety controls
- periodic red-team exercises for agent orchestration

## Verification Plan

- run seeded poisoning prompts and validate policy denies risky tools
- verify only user-authorized intents can invoke privileged tools
- audit traceability from retrieval chunk to action decision
