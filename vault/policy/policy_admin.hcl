# creating admin role in vault/cubbyhole

path "cubbyhole/approle_role" {
  capabilities = [ "create", "read", "update", "delete" ]
}

path "cubbyhole/approle_secret" {
  capabilities = [ "create", "read", "update", "delete" ]
}
