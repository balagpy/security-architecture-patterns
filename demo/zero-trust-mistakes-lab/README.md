# zero-trust-mistakes-lab

This lab simulates a common zero-trust implementation gap: strong edge identity, weak east-west service identity.

## Components

- `service-b-vulnerable` on `:8602`
- `service-b-mitigated` on `:8603`
- `service-a-to-vuln` on `:8611`
- `service-a-to-mit` on `:8612`

## Demonstrated Controls

- vulnerable: implicit trust for internal calls
- mitigated: explicit workload identity check for east-west access

## Run

```bash
./run-demo.sh
```
