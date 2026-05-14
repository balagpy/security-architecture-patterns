# Isolation Test Cases

1. Cross-tenant read probe by ID should return not found/deny.
2. Cache responses must remain tenant-scoped under key collision scenarios.
3. Async worker must reject jobs with missing/invalid tenant context.
4. Direct DB query path should enforce RLS policy.
5. Admin path should still enforce tenant boundary where applicable.
