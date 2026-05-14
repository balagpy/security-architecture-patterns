# Cache Namespacing Pattern

Use tenant-scoped cache keys for all shared-cache objects.

Good:
- `tenant:{tenant_id}:invoice:{id}`
- `tenant:{tenant_id}:user:{id}:permissions`

Avoid:
- `invoice:{id}`
- `user:{id}:permissions`
