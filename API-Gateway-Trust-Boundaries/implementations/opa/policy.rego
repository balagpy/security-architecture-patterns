package gateway.authz

default allow := false

allow if {
  input.caller_identity == "gateway"
  input.header_signature_valid == true
  input.role in {"user", "admin"}
}
