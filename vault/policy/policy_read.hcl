# creating reading access rights to vault

path "secret/django/oauth_api" {
  capabilities = [ "read" ]
}

path "secret/django/blockchain_api" {
  capabilities = [ "read" ]
}

path "secret/django/djkey_api" {
  capabilities = [ "read" ]
}

path "dbs/creds/ourdb-admin" {
  capabilities = [ "read" ]
}
