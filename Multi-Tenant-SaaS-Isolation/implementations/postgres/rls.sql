-- Example row-level security policy pattern
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_invoices ON invoices
USING (tenant_id = current_setting('app.tenant_id', true));

-- App must set: SET app.tenant_id = '<tenant-id>' per request context.
