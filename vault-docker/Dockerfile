FROM vault:latest

ENV VAULT_ADDR='http://0.0.0.0:8200'

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY config/vault-config.hcl /vault/config/vault-config.hcl

EXPOSE 8200

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
