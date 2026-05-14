import os
import time

import jwt
from flask import Flask, jsonify, request

app = Flask(__name__)

INSTANCE = os.getenv("INSTANCE_NAME", "oauth-api")
MODE = os.getenv("MODE", "vulnerable")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
EXPECTED_ISS = "lab-idp"
EXPECTED_AUD = "service-a"


def now() -> int:
    return int(time.time())


def issue_token(token_kind: str, aud: str, sub: str) -> str:
    claims = {
        "sub": sub,
        "iss": EXPECTED_ISS,
        "aud": aud,
        "iat": now(),
        "exp": now() + 3600,
        "scope": "read:profile" if token_kind == "access" else "openid profile",
        "token_use": token_kind,
    }
    return jwt.encode(claims, JWT_SECRET, algorithm="HS256")


def parse_token_from_header() -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise ValueError("missing bearer token")
    return auth[len("Bearer ") :].strip()


@app.get("/health")
def health():
    return jsonify({"ok": True, "instance": INSTANCE, "mode": MODE})


@app.post("/issue")
def issue():
    body = request.get_json(silent=True) or {}
    token_kind = body.get("token_kind", "access")
    aud = body.get("aud", EXPECTED_AUD)
    sub = body.get("sub", "alice")

    if token_kind not in {"access", "id"}:
        return jsonify({"error": "token_kind must be access or id"}), 400

    token = issue_token(token_kind, aud, sub)
    return jsonify({"token": token, "token_kind": token_kind, "aud": aud, "mode": MODE, "instance": INSTANCE})


@app.get("/resource")
def resource():
    try:
        token = parse_token_from_header()
    except Exception as exc:
        return jsonify({"error": str(exc)}), 401

    if MODE == "vulnerable":
        # Vulnerable: verifies signature/expiry but does not enforce intended audience or token use.
        try:
            claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        except Exception as exc:
            return jsonify({"error": f"invalid token: {exc}"}), 401

        return jsonify(
            {
                "allowed": True,
                "path": "vulnerable_loose_validation",
                "instance": INSTANCE,
                "mode": MODE,
                "claims": {"sub": claims.get("sub"), "aud": claims.get("aud"), "token_use": claims.get("token_use")},
            }
        )

    # Mitigated: strict issuer + audience + token_use checks.
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], issuer=EXPECTED_ISS, audience=EXPECTED_AUD)
    except Exception as exc:
        return jsonify({"error": f"invalid token: {exc}", "instance": INSTANCE, "mode": MODE}), 401

    if claims.get("token_use") != "access":
        return jsonify({"error": "invalid token_use for API", "instance": INSTANCE, "mode": MODE}), 401

    return jsonify(
        {
            "allowed": True,
            "path": "mitigated_strict_validation",
            "instance": INSTANCE,
            "mode": MODE,
            "claims": {"sub": claims.get("sub"), "aud": claims.get("aud"), "token_use": claims.get("token_use")},
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
