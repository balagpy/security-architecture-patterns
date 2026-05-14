package oauth.validation

default allow := false

allow if {
  input.claims.iss == input.expected_issuer
  input.claims.aud == input.expected_audience
  input.claims.token_use == "access"
  required_scope_present
}

required_scope_present if {
  some s
  s := input.required_scopes[_]
  s in input.claims.scopes
}
