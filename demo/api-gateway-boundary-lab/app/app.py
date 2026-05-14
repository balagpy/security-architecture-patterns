import hashlib
import hmac
import os
import time

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

ROLE = os.getenv("ROLE", "backend")
INSTANCE = os.getenv("INSTANCE_NAME", "service")
MODE = os.getenv("MODE", "vulnerable")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
GATEWAY_SIGNING_SECRET = os.getenv("GATEWAY_SIGNING_SECRET", "gateway-dev-secret")


def sign_forwarded_identity(user_id: str, role: str, ts: str) -> str:
    msg = f"{user_id}|{role}|{ts}".encode()
    return hmac.new(GATEWAY_SIGNING_SECRET.encode(), msg, hashlib.sha256).hexdigest()


def is_fresh(ts: str, max_skew_seconds: int = 60) -> bool:
    try:
        t = int(ts)
    except ValueError:
        return False
    return abs(int(time.time()) - t) <= max_skew_seconds


@app.get("/health")
def health():
    return jsonify({"ok": True, "role": ROLE, "instance": INSTANCE, "mode": MODE})


@app.get("/public")
def public():
    return jsonify({"message": "public endpoint", "instance": INSTANCE, "mode": MODE})


@app.get("/admin")
def admin():
    if ROLE == "gateway":
        # Gateway simulates auth result and forwards identity context headers.
        user = request.args.get("user", "alice")
        role = request.args.get("role", "user")
        ts = str(int(time.time()))
        sig = sign_forwarded_identity(user, role, ts)
        resp = requests.get(
            f"{BACKEND_URL}/admin",
            headers={
                "X-User-Id": user,
                "X-Role": role,
                "X-Auth-Ts": ts,
                "X-Auth-Signature": sig,
                "X-Forwarded-By": "gateway",
            },
            timeout=5,
        )
        return (resp.text, resp.status_code, {"content-type": "application/json"})

    # Backend behavior.
    role = request.headers.get("X-Role", "")

    if MODE == "vulnerable":
        if role == "admin":
            return jsonify(
                {
                    "allowed": True,
                    "path": "vulnerable_header_trust",
                    "message": "sensitive admin data",
                    "instance": INSTANCE,
                    "mode": MODE,
                    "role_seen": role,
                }
            )
        return jsonify({"allowed": False, "reason": "admin required", "instance": INSTANCE, "mode": MODE}), 403

    # Mitigated: require provenance and signature verification.
    forwarded_by = request.headers.get("X-Forwarded-By", "")
    user = request.headers.get("X-User-Id", "")
    ts = request.headers.get("X-Auth-Ts", "")
    sig = request.headers.get("X-Auth-Signature", "")

    if forwarded_by != "gateway":
        return jsonify({"allowed": False, "reason": "untrusted caller", "instance": INSTANCE, "mode": MODE}), 403

    if not is_fresh(ts):
        return jsonify({"allowed": False, "reason": "stale auth context", "instance": INSTANCE, "mode": MODE}), 403

    expected = sign_forwarded_identity(user, role, ts)
    if not hmac.compare_digest(sig, expected):
        return jsonify({"allowed": False, "reason": "invalid signature", "instance": INSTANCE, "mode": MODE}), 403

    if role != "admin":
        return jsonify({"allowed": False, "reason": "admin required", "instance": INSTANCE, "mode": MODE}), 403

    return jsonify(
        {
            "allowed": True,
            "path": "mitigated_verified_forwarded_identity",
            "message": "sensitive admin data",
            "instance": INSTANCE,
            "mode": MODE,
            "user": user,
            "role_seen": role,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
