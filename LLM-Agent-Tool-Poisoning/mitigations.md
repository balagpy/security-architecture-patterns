# Mitigations - LLM Agent Tool Poisoning

## Goals

- Prevent untrusted content from directly authorizing tool execution.
- Minimize blast radius of policy or reasoning mistakes.
- Preserve auditable decision provenance end-to-end.

## Strategy Comparison

| Strategy | Latency Impact | Complexity | Safety Gain | Scalability |
| --- | --- | --- | --- | --- |
| Intent-to-tool allowlist policy | Low-Medium | Medium | High | High |
| Trust-tiered context separation | Medium | Medium | Medium-High | High |
| Step-up approval for high-risk tools | Medium-High | Low-Medium | High | Medium |
| Sandboxed runtime + scoped credentials | Medium | High | High | Medium-High |
| Hybrid (all above) | Medium-High | High | Very High | Medium |

## Pattern Options

1. Intent-to-tool allowlist policy

- Design summary: map user-approved intents to explicit allowed tool classes.
- Implementation complexity: Medium.
- Performance tradeoff: low runtime cost, medium policy maintenance effort.
- Residual risk: unknown intent classes can bypass expectations without update discipline.

2. Trust-tiered context separation

- Design summary: treat retrieval as untrusted data, separate from system/policy instructions.
- Implementation complexity: Medium.
- Performance tradeoff: moderate prompt and orchestration complexity.
- Residual risk: source trust misclassification.

3. Step-up confirmation for high-risk actions

- Design summary: require explicit approval for privileged operations.
- Implementation complexity: Low-Medium.
- Performance tradeoff: interaction latency and operator fatigue risk.
- Residual risk: social engineering or weak approval UX.

4. Tool capability sandboxing

- Design summary: least-privilege execution, filesystem scoping, egress controls, ephemeral tool credentials.
- Implementation complexity: High.
- Performance tradeoff: infrastructure and operational overhead.
- Residual risk: sandbox misconfiguration or scope drift.

## Recommended Sequence

1. Immediate

- Enforce deny-by-default intent-to-tool policy.
- Add approval gate for high-risk tool classes.
- Capture provenance for each tool decision.

2. Medium-term

- Implement trust-tiered retrieval handling.
- Add recurring adversarial tool-use test suite.

3. Long-term

- Codify agent safety policy-as-code with change governance.
- Run periodic red-team exercises focused on orchestration abuse.

## When Not to Use a Pattern

- Do not use broad unrestricted tool access in production-like environments.
- Do not depend on approval gates alone without strong policy and sandbox controls.
- Do not centralize all safety in prompting while ignoring runtime enforcement.

## Verification Plan

- Run seeded prompt-injection scenarios and verify high-risk tool denial.
- Validate that only approved intents invoke privileged tools.
- Audit end-to-end traceability from retrieved content to execution decision.
- Simulate sandbox escape attempts and scope drift regressions.
