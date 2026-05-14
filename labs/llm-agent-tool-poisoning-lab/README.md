# llm-agent-tool-poisoning-lab

This lab simulates prompt/tool poisoning in agent systems.

## Components

- `agent-vulnerable` on `:8501`
- `agent-mitigated` on `:8502`

## Demonstrated Controls

- intent-to-tool allowlist policy
- denial of unapproved high-risk tools
- optional step-up confirmation model

## Run

```bash
./run-demo.sh
```
