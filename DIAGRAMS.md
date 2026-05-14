# Diagram Standards

Repository standard is Mermaid source + SVG render output.

## Per Case Study

Required files:
- `diagrams/architecture.mmd`
- `diagrams/attack-flow.mmd`
- `architecture.svg`
- `attack-flow.svg`

Notes:
- Mermaid (`.mmd`) is the editable source of truth.
- SVG is the publication artifact for README viewing and sharing.
- PNG is optional and only needed for platforms that cannot render SVG.

## Rendering

If Mermaid CLI is available, render from each case-study directory:

```bash
mmdc -i diagrams/architecture.mmd -o architecture.svg
mmdc -i diagrams/attack-flow.mmd -o attack-flow.svg
```
