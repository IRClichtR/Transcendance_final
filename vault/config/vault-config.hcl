# listener config
listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 1
#  tls_cert_file = "/tls-certificates/cert.pem
#  tls_key_file = "/tls-certificates/key.pem"
}

# storage config
storage "file" {
  path = "/vault/data"
}

# API address
api_addr = "http://10.24.104.7:8200"

# enabling run in containers
disable_mlock = true

# User interface
ui = true