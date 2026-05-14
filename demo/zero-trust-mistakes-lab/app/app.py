import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
ROLE = os.getenv("ROLE", "service-b")
MODE = os.getenv("MODE", "vulnerable")
INSTANCE = os.getenv("INSTANCE_NAME", "service")
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://service-b:8000")
WORKLOAD_TOKEN = os.getenv("WORKLOAD_TOKEN", "trusted-a-token")


@app.get("/health")
def health():
    return jsonify({"ok": True, "role": ROLE, "mode": MODE, "instance": INSTANCE})


@app.get("/pivot")
def pivot():
    if ROLE != "service-a":
        return jsonify({"error": "endpoint only valid on service-a"}), 400

    token = request.args.get("token", "")
    headers = {}
    if token:
        headers["X-Workload-Token"] = token

    resp = requests.get(f"{SERVICE_B_URL}/sensitive", headers=headers, timeout=5)
    return (resp.text, resp.status_code, {"content-type": "application/json"})


@app.get("/sensitive")
def sensitive():
    if ROLE != "service-b":
        return jsonify({"error": "endpoint only valid on service-b"}), 400

    if MODE == "vulnerable":
        # Vulnerable: implicit internal trust, no workload identity verification.
        return jsonify(
            {
                "allowed": True,
                "decision_path": "vulnerable_implicit_internal_trust",
                "data": "sensitive-east-west-data",
                "instance": INSTANCE,
            }
        )

    presented = request.headers.get("X-Workload-Token", "")
    if presented != WORKLOAD_TOKEN:
        return jsonify(
            {
                "allowed": False,
                "reason": "missing/invalid workload identity",
                "decision_path": "mitigated_workload_identity_check",
                "instance": INSTANCE,
            }
        ), 403

    return jsonify(
        {
            "allowed": True,
            "decision_path": "mitigated_verified_workload_identity",
            "data": "sensitive-east-west-data",
            "instance": INSTANCE,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
