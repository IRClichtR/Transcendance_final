# base image
FROM hashicorp/vault

#download dependencies
RUN apk --no-cache add \
		bash \
		ca-certificates \
		wget \
		curl \
		unzip \
		coreutils		# for shuf cmd

# Keys and cert gen
RUN mkdir -p vault/tls-certificates
# RUN openssl req -newkey rsa:2048 -x509 -nodes -days 42 -keyout /vault/tls-certificates/key.pem -out /vault/tls-certificates/cert.pem -config san.cnf

# Importing tokens and certificates
COPY tls-certificates/cert.pem /vault/tls-certificates/cert.pem
COPY tls-certificates/key.pem /vault/tls-certificates/key.pem

# Ensuring correct rights
RUN chmod 644 /vault/tls-certificates/cert.pem /vault/tls-certificates/key.pem

# Policies and script import
# COPY policy.hcl /policy.hcl
COPY config/vault-config.hcl /vault/config/vault-config.hcl

COPY entrypoint.sh /vault/entrypoint.sh
RUN chmod +x /vault/entrypoint.sh


# COPY policy-credentials-token.hcl /policy-credentials-token.hcl
# COPY elk-credentials-token.hcl /elk-credentials-token.hcl
# COPY elk-admin-token.hcl /elk-admin-token.hcl


# exposing port 8200
EXPOSE 8200
EXPOSE 8201

# running vault
ENTRYPOINT ["/vault/entrypoint.sh"]


# FROM hashicorp/vault

# RUN mkdir -p /vault

# COPY vault-init.sh /usr/local/bin/vault-init.sh

# COPY config.hcl /vault/config/config.hcl

# RUN chmod 755 /usr/local/bin/vault-init.sh

# RUN [ "/usr/local/bin/vault-init.sh" ]

# updating path
# ENV PATH="PATH=$PATH:$PWD/vault"

# ENTRYPOINT [ "vault" ]
# CMD [ "server", "-config=/vault/config" ]
