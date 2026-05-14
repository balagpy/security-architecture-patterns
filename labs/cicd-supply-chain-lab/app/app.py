import os

from flask import Flask, jsonify, request

app = Flask(__name__)
MODE = os.getenv("MODE", "vulnerable")
INSTANCE = os.getenv("INSTANCE_NAME", "cicd-lab")


@app.get("/health")
def health():
    return jsonify({"ok": True, "mode": MODE, "instance": INSTANCE})


@app.post("/evaluate")
def evaluate():
    body = request.get_json(silent=True) or {}
    action_ref = body.get("action_ref", "org/action@v1")
    artifact_signed = bool(body.get("artifact_signed", False))

    if MODE == "vulnerable":
        # Vulnerable policy: mutable action refs and unsigned artifacts are tolerated.
        return jsonify(
            {
                "allowed": True,
                "decision_path": "vulnerable_permissive_policy",
                "details": {
                    "action_ref": action_ref,
                    "artifact_signed": artifact_signed,
                },
            }
        )

    # Mitigated policy: require immutable action pin + signed artifact.
    pinned = "@sha256:" in action_ref or "@" in action_ref and len(action_ref.split("@", 1)[1]) >= 40
    if not pinned:
        return jsonify({"allowed": False, "reason": "action reference not immutable/pinned", "action_ref": action_ref}), 403

    if not artifact_signed:
        return jsonify({"allowed": False, "reason": "artifact provenance/signature missing"}), 403

    return jsonify(
        {
            "allowed": True,
            "decision_path": "mitigated_supply_chain_policy",
            "details": {
                "action_ref": action_ref,
                "artifact_signed": artifact_signed,
            },
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
