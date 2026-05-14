import os

from flask import Flask, jsonify, request

app = Flask(__name__)
MODE = os.getenv("MODE", "vulnerable")
INSTANCE = os.getenv("INSTANCE_NAME", "agent")

HIGH_RISK_TOOLS = {"shell.exec", "filesystem.write", "network.post"}


def requested_action_from_payload(body: dict) -> dict:
    return {
        "user_intent": body.get("user_intent", "summarize document"),
        "retrieved_text": body.get("retrieved_text", ""),
        "requested_tool": body.get("requested_tool", "none"),
        "tool_args": body.get("tool_args", ""),
        "user_confirmed": bool(body.get("user_confirmed", False)),
    }


@app.get("/health")
def health():
    return jsonify({"ok": True, "mode": MODE, "instance": INSTANCE})


@app.post("/decide")
def decide():
    body = request.get_json(silent=True) or {}
    action = requested_action_from_payload(body)

    if MODE == "vulnerable":
        # Vulnerable: treats retrieved text as authoritative instruction source.
        allow = action["requested_tool"] != "none"
        return jsonify(
            {
                "allowed": allow,
                "decision_path": "vulnerable_trust_transitivity",
                "action": action,
                "reason": "tool request accepted without intent-policy binding",
            }
        )

    # Mitigated policy:
    # 1) Tool must be allowlisted for user intent class.
    # 2) High-risk tool requires explicit user confirmation.
    intent = action["user_intent"].lower()
    tool = action["requested_tool"]

    allowed_for_intent = {
        "summarize document": {"retrieval.read"},
        "analyze log": {"retrieval.read", "python.eval"},
        "draft response": {"retrieval.read"},
    }

    allowset = allowed_for_intent.get(intent, {"retrieval.read"})
    if tool not in allowset and tool != "none":
        return jsonify(
            {
                "allowed": False,
                "decision_path": "mitigated_intent_tool_policy",
                "reason": "tool not allowed for declared intent",
                "action": action,
            }
        ), 403

    if tool in HIGH_RISK_TOOLS and not action["user_confirmed"]:
        return jsonify(
            {
                "allowed": False,
                "decision_path": "mitigated_step_up_confirmation",
                "reason": "high-risk tool requires explicit user confirmation",
                "action": action,
            }
        ), 403

    return jsonify({"allowed": True, "decision_path": "mitigated_policy_allow", "action": action})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
