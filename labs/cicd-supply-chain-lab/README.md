# cicd-supply-chain-lab

This lab simulates CI/CD policy decisions for supply-chain risk.

## Components

- `policy-vulnerable` on `:8401`
- `policy-mitigated` on `:8402`

## Demonstrated Controls

- reject mutable/unpinned action references
- reject unsigned artifacts without provenance

## Run

```bash
./run-demo.sh
```
