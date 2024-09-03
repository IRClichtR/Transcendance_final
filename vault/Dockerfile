# base image
FROM hashicorp/vault

#download dependencies
RUN apk --no-cache add \
		bash \
		ca-certificates \
		wget \
		curl \
		unzip \
		coreutils \
		openssl 

# Keys and cert gen
# Verbose: create directory for TLS certificates
RUN echo "Creating directory /vault/tls-certificates..." && \
	mkdir -p /vault/tls-certificates

# # Importing tokens and certificates
# COPY tls-certificates/cert.pem /tls-certificates/cert.pem
# COPY tls-certificates/key.pem /tls-certificates/key.pem
COPY tls-certificates/san.cnf /tls-certificates/san.cnf

RUN echo "Generating TLS keys and certificates..." && \
	openssl req -newkey rsa:2048 -x509 -nodes -days 42 \
	-keyout /tls-certificates/key.pem \
	-out /tls-certificates/cert.pem \
	-config /tls-certificates/san.cnf

# Verbose: set permissions
RUN echo "Setting permissions on cert and key files..." && \
	chmod 644 /tls-certificates/cert.pem /tls-certificates/key.pem

# Copy Vault configuration
# RUN echo "Copying Vault configuration..." && \
#     mkdir -p /vault/config

COPY vault-config.hcl /vault-config.hcl

# Policies and script import
# COPY policy.hcl /policy.hcl

COPY entrypoint.sh /vault/entrypoint.sh
RUN chmod +x /vault/entrypoint.sh

# COPY policy-credentials-token.hcl /policy-credentials-token.hcl

# exposing port 8200
# EXPOSE 8200
# EXPOSE 8201

# Verbose: final message before running entrypoint
RUN echo "Vault Docker image is built successfully."

# running vault
ENTRYPOINT ["/vault/entrypoint.sh"]
