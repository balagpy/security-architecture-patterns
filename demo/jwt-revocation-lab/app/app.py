import os
import time
import uuid
from typing import Dict

import jwt
import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

INSTANCE_NAME = os.getenv("INSTANCE_NAME", "api")
MODE = os.getenv("MODE", "vulnerable")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
ACCESS_TTL_SECONDS = int(os.getenv("ACCESS_TTL_SECONDS", "300"))
REVOCATION_CACHE_TTL_SECONDS = int(os.getenv("REVOCATION_CACHE_TTL_SECONDS", "20"))

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
local_revocation_cache: Dict[str, float] = {}
last_refresh = 0.0


def now() -> int:
    return int(time.time())


def mint_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "jti": str(uuid.uuid4()),
        "iat": now(),
        "exp": now() + ACCESS_TTL_SECONDS,
        "iss": "jwt-revocation-lab",
        "aud": "lab-api",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def parse_bearer_token() -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return ""
    return auth[len("Bearer ") :].strip()


def decode_token(token: str):
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=["HS256"],
        audience="lab-api",
        issuer="jwt-revocation-lab",
    )


def revoke_jti(jti: str, exp: int):
    ttl = max(1, exp - now())
    r.setex(f"revoked:{jti}", ttl, "1")


def refresh_local_cache_if_needed():
    global last_refresh
    if now() - last_refresh < REVOCATION_CACHE_TTL_SECONDS:
        return
    local_revocation_cache.clear()
    for key in r.scan_iter(match="revoked:*"):
        local_revocation_cache[key.split(":", 1)[1]] = time.time()
    last_refresh = now()


def is_revoked(jti: str) -> bool:
    if MODE == "vulnerable":
        # Vulnerable behavior: relies on periodic local cache refresh, creating stale windows.
        refresh_local_cache_if_needed()
        return jti in local_revocation_cache

    # Mitigated behavior: always checks centralized revocation state synchronously.
    return r.exists(f"revoked:{jti}") == 1


@app.get("/health")
def health():
    return jsonify({"ok": True, "instance": INSTANCE_NAME, "mode": MODE})


@app.post("/issue")
def issue():
    body = request.get_json(silent=True) or {}
    subject = body.get("sub", "user-123")
    token = mint_token(subject)
    claims = decode_token(token)
    return jsonify(
        {
            "token": token,
            "claims": claims,
            "instance": INSTANCE_NAME,
            "mode": MODE,
        }
    )


@app.post("/revoke")
def revoke():
    token = parse_bearer_token()
    if not token:
        return jsonify({"error": "missing bearer token"}), 400
    try:
        claims = decode_token(token)
    except Exception as exc:
        return jsonify({"error": f"invalid token: {exc}"}), 401

    revoke_jti(claims["jti"], claims["exp"])
    return jsonify(
        {
            "revoked_jti": claims["jti"],
            "revoked_at": now(),
            "instance": INSTANCE_NAME,
            "mode": MODE,
        }
    )


@app.get("/resource")
def resource():
    token = parse_bearer_token()
    if not token:
        return jsonify({"error": "missing bearer token"}), 401

    try:
        claims = decode_token(token)
    except Exception as exc:
        return jsonify({"error": f"invalid token: {exc}"}), 401

    if is_revoked(claims["jti"]):
        return jsonify(
            {
                "allowed": False,
                "reason": "token revoked",
                "jti": claims["jti"],
                "instance": INSTANCE_NAME,
                "mode": MODE,
            }
        ), 401

    return jsonify(
        {
            "allowed": True,
            "message": "protected data",
            "sub": claims["sub"],
            "jti": claims["jti"],
            "instance": INSTANCE_NAME,
            "mode": MODE,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
