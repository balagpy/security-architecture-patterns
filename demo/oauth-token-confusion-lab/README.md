# oauth-token-confusion-lab

This lab shows two OAuth token confusion failures:
- ID token accepted as API access token
- access token with wrong audience accepted by API

## Components

- `api-vulnerable` on `:8301`
- `api-mitigated` on `:8302`

## Mitigated Checks

- strict `iss` and `aud`
- strict `token_use=access` for API endpoints

## Run

```bash
./run-demo.sh
```
