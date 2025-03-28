# listener config
listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 0
  tls_cert_file = "/tls-certificates/cert.pem"
  tls_key_file = "/tls-certificates/key.pem"
}

# storage config
storage "file" {
  path = "/vault/data"
}

# API address
api_addr = "https://localhost:8200"
cluster_addr = "https://localhost:8201"

# enabling run in containers
disable_mlock = true

# User interface
ui = true
