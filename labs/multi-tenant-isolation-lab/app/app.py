import os
import time
from copy import deepcopy

import jwt
from flask import Flask, jsonify, request

app = Flask(__name__)

INSTANCE_NAME = os.getenv("INSTANCE_NAME", "api")
MODE = os.getenv("MODE", "vulnerable")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")

INVOICES = {
    "tenant-a": {"42": {"id": "42", "tenant_id": "tenant-a", "amount": 1200, "owner": "alice"}},
    "tenant-b": {"42": {"id": "42", "tenant_id": "tenant-b", "amount": 9900, "owner": "bob"}},
}

# Intentional vulnerable cache shape: key is invoice id only, not tenant+id.
VULN_CACHE = {"42": deepcopy(INVOICES["tenant-b"]["42"])}


def now() -> int:
    return int(time.time())


def issue_token(tenant_id: str, user: str) -> str:
    payload = {
        "sub": user,
        "tenant_id": tenant_id,
        "iat": now(),
        "exp": now() + 3600,
        "iss": "multi-tenant-lab",
        "aud": "tenant-api",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def parse_token() -> dict:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise ValueError("missing bearer token")
    token = auth[len("Bearer ") :].strip()
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=["HS256"],
        audience="tenant-api",
        issuer="multi-tenant-lab",
    )


@app.get("/health")
def health():
    return jsonify({"ok": True, "instance": INSTANCE_NAME, "mode": MODE})


@app.post("/issue")
def issue():
    body = request.get_json(silent=True) or {}
    tenant_id = body.get("tenant_id", "tenant-a")
    user = body.get("user", "alice")
    token = issue_token(tenant_id, user)
    return jsonify({"token": token, "tenant_id": tenant_id, "instance": INSTANCE_NAME, "mode": MODE})


@app.get("/invoice/<invoice_id>")
def get_invoice(invoice_id: str):
    try:
        claims = parse_token()
    except Exception as exc:
        return jsonify({"error": str(exc)}), 401

    tenant_id = claims["tenant_id"]

    if MODE == "vulnerable":
        # Vulnerability: cache lookup ignores tenant namespace.
        cached = VULN_CACHE.get(invoice_id)
        if cached:
            return jsonify(
                {
                    "allowed": True,
                    "source": "vulnerable_cache",
                    "requested_by_tenant": tenant_id,
                    "data": cached,
                    "instance": INSTANCE_NAME,
                    "mode": MODE,
                }
            )

        # Additional vulnerability: fallback lookup by id across tenants.
        for t, tenant_rows in INVOICES.items():
            if invoice_id in tenant_rows:
                return jsonify(
                    {
                        "allowed": True,
                        "source": "cross_tenant_scan",
                        "requested_by_tenant": tenant_id,
                        "data": tenant_rows[invoice_id],
                        "instance": INSTANCE_NAME,
                        "mode": MODE,
                    }
                )

        return jsonify({"error": "not found"}), 404

    # Mitigated path: strict tenant-scoped lookup.
    tenant_rows = INVOICES.get(tenant_id, {})
    row = tenant_rows.get(invoice_id)
    if not row:
        return jsonify({"error": "not found within tenant scope", "instance": INSTANCE_NAME, "mode": MODE}), 404

    return jsonify(
        {
            "allowed": True,
            "source": "tenant_scoped_lookup",
            "requested_by_tenant": tenant_id,
            "data": row,
            "instance": INSTANCE_NAME,
            "mode": MODE,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
