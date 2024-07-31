listener "tcp" {
address = "0.0.0.0:8200"
tls_disable = 0
tls_cert_file = "/tls-certificates/cert.pem"
tls_key_file = "/tls-certificates/key.pem"
}
storage "file" {
path = ""
}
ui = true