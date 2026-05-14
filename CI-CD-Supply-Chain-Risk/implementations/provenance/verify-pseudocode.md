# Provenance Gate Pseudocode

```text
if artifact.signature_invalid: reject
if artifact.attestation.missing: reject
if artifact.source_repo != expected_repo: reject
if artifact.builder_identity not trusted_builders: reject
allow_deploy
```
