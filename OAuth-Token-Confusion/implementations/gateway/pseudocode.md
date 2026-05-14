# Gateway Validation Pseudocode

```text
if token.signature_invalid: deny
if token.issuer != expected_issuer: deny
if token.audience != route.expected_audience: deny
if token_use != "access": deny
if required_scope not in token.scopes: deny
allow
```
