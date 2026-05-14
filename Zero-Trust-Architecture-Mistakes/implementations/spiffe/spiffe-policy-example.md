# SPIFFE Identity Policy Example

```text
allowed_principals_for_service_b:
  - spiffe://prod/ns/platform/sa/service-a
blocked_principals:
  - spiffe://prod/ns/default/sa/*
```
