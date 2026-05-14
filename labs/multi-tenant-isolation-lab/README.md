# multi-tenant-isolation-lab

This lab demonstrates a common SaaS isolation failure where tenant context is not enforced consistently.

## Components

- `api-vulnerable` on `:8101`
- `api-mitigated` on `:8102`

## Vulnerable Behavior

- cache key is only `invoice_id`, not `tenant_id + invoice_id`
- fallback query scans by id across tenant partitions
- Tenant A can receive Tenant B invoice data for overlapping IDs

## Mitigated Behavior

- strict tenant-scoped lookup based on JWT `tenant_id`
- no cross-tenant scan path

## Run

```bash
docker compose up --build
```

Or run the guided demo:

```bash
./run-demo.sh
```

## Expected Result

With a Tenant-A token querying invoice `42`:
- vulnerable service may return record with `tenant_id = tenant-b`
- mitigated service returns only tenant-a data or tenant-scoped not-found
