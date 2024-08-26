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
# COPY vault.hcl /vault.hcl
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Importing tokens and certificates
COPY tls-certificates /tls-certificates
# COPY policy-credentials-token.hcl /policy-credentials-token.hcl
# COPY elk-credentials-token.hcl /elk-credentials-token.hcl
# COPY elk-admin-token.hcl /elk-admin-token.hcl

# # vault version
# ENV VAULT_VERSION 0.10.3

# # create new dir
# RUN mkdir /vault



# # download and install Vault
# RUN wget --output-document=/tmp/vault.zip https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip && \
# 		unzip /tmp/vault.zip -d /vault && \
# 		rm -f /tmp/vault.zip && \
# 		chmod +x /vault


# updating path
ENV PATH="PATH=$PATH:$PWD/vault"


# add the config file
# COPY ./config/vault-config.json /vault/config/vault-config.json

# exposing port 8200
EXPOSE 8200

# running vault
# ENTRYPOINT ["vault"]

# Launching entrypoint-vault
CMD /entrypoint.sh

