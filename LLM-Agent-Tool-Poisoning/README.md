# LLM Agent Tool Poisoning and Trust Transitivity Failures

## Executive Summary


Agentic systems become risky when untrusted content can quietly influence tool execution. The model may treat retrieved text as instruction-like context, and if tooling permissions are broad, a single poisoned step can trigger high-impact actions.

The weak point is usually orchestration policy, not model intelligence alone.

## System Context

Typical agent architecture:
- orchestrator receives user goal
- model reads mixed-trust context (user input, retrieved docs, external pages)
- tool router selects and executes tools
- results loop back to model for next actions

Security invariant:
- untrusted content must never become implicit authority for tool execution

## Baseline Architecture

See `architecture.svg` (rendered) and `diagrams/architecture.mmd` (source).

![Architecture Diagram](./architecture.svg)

## Normal Flow

1. User submits objective.
2. Agent retrieves context.
3. Model proposes actions.
4. Policy guard evaluates tool request.
5. Approved tool executes with constrained scope.

## Failure Modes

1. Instruction injection from retrieved content
- malicious text says "run shell command" or "exfiltrate secrets"
- model follows as if system-authorized instruction

2. Over-broad tool permissions
- agent has filesystem/network/tool access unrelated to current task

3. Missing intent-to-action policy binding
- no explicit mapping from user intent to allowed tool classes

4. No provenance tracking
- execution logs do not show which source content triggered tool call

## Attack/Abuse Flow

See `attack-flow.svg` (rendered) and `diagrams/attack-flow.mmd` (source).

See `sequence.svg` (rendered) and `diagrams/sequence.mmd` (source).

![Attack Flow Diagram](./attack-flow.svg)

![Sequence Diagram](./sequence.svg)

## Impact

- Confidentiality: secret/file exfiltration through tool calls.
- Integrity: unauthorized modifications via command execution.
- Availability: destructive or expensive tool loops.
- Governance: inability to prove safe decision boundaries.

## Detection Opportunities

- tool calls whose justification text originates from untrusted retrieval chunks
- sudden jumps to high-risk tools without prior explicit user authorization
- deviations from expected tool-use policy per task type
- anomalous high-privilege tool invocation patterns

## Mitigation Strategy

See [mitigations.md](./mitigations.md).

## Why Existing Systems Fail


In practice, teams push autonomy before control maturity:

- Tool breadth is expanded to reduce human handoffs.
- Retrieval context and instruction context are not strongly separated.
- Policy checks are coarse and do not map tightly to user intent.
- Logging captures outputs but misses decision provenance.

That combination creates a path from convenience to compromise.

## Real Incident Correlation


Public red-team work and incident reporting repeatedly show:

- Prompt injection leading to unintended tool calls.
- Data exfiltration attempts through plugin/tool channels.
- Workflow hijack patterns originating from untrusted retrieved content.

The common failure mode is weak trust-tiering in the agent control plane.

## Evidence

Signals to collect for validation:

- Metrics: `time-to-final-reject`, `policy-deny-rate`, and cross-replica decision divergence.
- Logs: identity context, enforcement path, and reason code for allow/deny decisions.
- Tests: replay, propagation-delay, and failover behavior under sustained load.

## Practical Demo

Companion demo:

- [llm-agent-tool-poisoning-lab](../demo/llm-agent-tool-poisoning-lab/README.md)
- [Run script](../demo/llm-agent-tool-poisoning-lab/run-demo.sh)


## Known Limitations


- The demo abstracts away model-specific guardrail differences.
- It does not model full enterprise approval workflows or human-in-the-loop escalations.
- Production safety needs layered controls across prompting, policy, runtime, and audit.

## References

See [references.md](./references.md).
