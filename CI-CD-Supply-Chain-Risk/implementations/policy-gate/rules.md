# Workflow Policy Rules

- Reject mutable action refs (for example `@v1`) for privileged workflows.
- Reject workflows requesting broad token permissions by default.
- Reject workflows that expose secrets to untrusted PR contexts.
- Require approval for workflow changes touching deploy jobs.
