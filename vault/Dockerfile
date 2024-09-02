# base image
FROM hashicorp/vault

#download dependencies
RUN apk --no-cache add \
		bash \
		ca-certificates \
		wget \
		curl \
		unzip \
		coreutils 		# for shuf cmd
		# openssl 		# for certs and keys

# Keys and cert gen
# Verbose: create directory for TLS certificates
RUN echo "Creating directory /vault/tls-certificates..." && \
	mkdir -p /vault/tls-certificates

# Importing tokens and certificates
COPY tls-certificates/cert.pem /tls-certificates/cert.pem
COPY tls-certificates/key.pem /tls-certificates/key.pem

# Verbose: set permissions
RUN echo "Setting permissions on cert and key files..." && \
	chmod 644 /tls-certificates/cert.pem /tls-certificates/key.pem


# RUN echo "Generating TLS keys and certificates..." && \
# 	openssl req -newkey rsa:2048 -x509 -nodes -days 42 \
# 	-keyout /vault/tls-certificates/key.pem \
# 	-out /vault/tls-certificates/cert.pem \
# 	-config san.cnf




# Copy Vault configuration
# RUN echo "Copying Vault configuration..." && \
#     mkdir -p /vault/config

COPY vault-config.hcl /vault-config.hcl




# Policies and script import
# COPY policy.hcl /policy.hcl

COPY entrypoint.sh /vault/entrypoint.sh
RUN chmod +x /vault/entrypoint.sh


# COPY policy-credentials-token.hcl /policy-credentials-token.hcl
# COPY elk-credentials-token.hcl /elk-credentials-token.hcl
# COPY elk-admin-token.hcl /elk-admin-token.hcl


# exposing port 8200
# EXPOSE 8200
# EXPOSE 8201

# Verbose: final message before running entrypoint
RUN echo "Vault Docker image is built successfully."


# Default command: start a shell for inspection or run the entrypoint
# CMD ["bash", "-c", "echo 'Container started. Use exec to inspect.' && exec /vault/entrypoint.sh"]


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
