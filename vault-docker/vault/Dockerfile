# base image
FROM hashicorp/vault

#download dependencies
RUN apk --no-cache add \
		bash \
		ca-certificates \
		wget \
		curl \
		unzip

# Policies and script import
# COPY policy.hcl /policy.hcl
COPY config/vault-config.hcl /config/vault-config.hcl

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Importing tokens and certificates
COPY tls-certificates /tls-certificates
# COPY policy-credentials-token.hcl /policy-credentials-token.hcl
# COPY elk-credentials-token.hcl /elk-credentials-token.hcl
# COPY elk-admin-token.hcl /elk-admin-token.hcl

# updating path
ENV PATH="PATH=$PATH:$PWD/vault"


# exposing port 8200
EXPOSE 8200

# running vault
# ENTRYPOINT ["vault"]


# FROM hashicorp/vault

# RUN mkdir -p /vault

# COPY vault-init.sh /usr/local/bin/vault-init.sh

# COPY config.hcl /vault/config/config.hcl

# RUN chmod 755 /usr/local/bin/vault-init.sh

# RUN [ "/usr/local/bin/vault-init.sh" ]

# ENTRYPOINT [ "vault" ]
# CMD [ "server", "-config=/vault/config" ]
