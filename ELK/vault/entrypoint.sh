#!/bin/bash

# Start Vault in server mode with the specified configuration
vault server -config=/vault/config/vault-config.hcl &
VAULT_PID=$!

# Wait for Vault to start
sleep 5

# Initialize Vault if not already initialized
if [ ! -f /vault/init.file ]; then
  vault operator init -key-shares=1 -key-threshold=1 > /vault/init.file
  cat /vault/init.file | grep 'Unseal Key 1:' | awk '{print $NF}' > /vault/unseal.key
  cat /vault/init.file | grep 'Initial Root Token:' | awk '{print $NF}' > /vault/root.token
fi

# Unseal Vault
vault operator unseal $(cat /vault/unseal.key)

# Wait for Vault process to finish
wait $VAULT_PID



# VAULT_ADDR="http://0.0.0.0:8200"

# echo "Initializing Vault... $VAULT_ADDR"


# # Check if vault is already initialized
# init_output=$(docker exec vault vault operator init)
# if [ $? -ne 0 ]; then
# 	echo "[ERROR] Vault initialization failed"
# 	exit 1
# fi

# # If vault is already initialized init_output will get the actual status
# echo "Unseal keys and root token: $init_output"
# unseal_key_1=$(echo "$init_output" | awk '/Unseal Key 1/ {print $4}')
# unseal_key_2=$(echo "$init_output" | awk '/Unseal Key 2/ {print $4}')
# unseal_key_3=$(echo "$init_output" | awk '/Unseal Key 3/ {print $4}')

# # unsealing keys
# echo "Unseal Key 1: $unseal_key_1"
# docker exec vault vault operator unseal $unseal_key_1
# if [ $? -ne 0 ]; then
# 	echo "Erreur lors du déverrouillage de Vault avec la clé $unseal_key_1"
# 	exit 1
# fi

# echo "Unseal Key 2: $unseal_key_2"
# docker exec vault vault operator unseal $unseal_key_2
# if [ $? -ne 0 ]; then
# 	echo "Erreur lors du déverrouillage de Vault avec la clé $unseal_key_2"
# 	exit 1
# fi

# echo "Unseal Key 3: $unseal_key_3"
# docker exec vault vault operator unseal $unseal_key_3
# if [ $? -ne 0 ]; then
# 	echo "Erreur lors du déverrouillage de Vault avec la clé $unseal_key_3"
# 	exit 1
# fi

# # Get root token
# root_token=$(echo "$init_output" | awk '/Initial Root Token/ {print $4}')
# echo "Root Token: $root_token"
# docker exec vault vault login $root_token
# if [ $? -ne 0 ]; then
# 	exit 1
# fi

# export VAULT_TOKEN=$root_token

# echo "Vérification du Secret Engine KV..."
# kv_enabled=$(docker exec vault vault secrets list | grep -E "^kv/")
# if [ -z "$kv_enabled" ]; then
# 	echo "Activation du Secret Engine KV version 2..."
# 	docker exec vault vault secrets enable -version=2 kv
# 	if [ $? -ne 0 ]; then
# 		echo "Erreur lors de l'activation du Secret Engine KV"
# 		exit 1
# 	fi
# else
# 	echo "Le Secret Engine KV est déjà activé."
# fi

# # path to adapt
# RELATIVE_PATH="../../.env.dev"

# # same same
# ENV_FILE=$(realpath "$(dirname "$0")/$RELATIVE_PATH")

# # modifying output messages
# echo "Vérification de l'existence du fichier .env..."
# if [ ! -f "$ENV_FILE" ]; then
# 	echo "Le fichier .env n'existe pas à l'emplacement spécifié."
# 	exit 1
# fi

# echo "Lecture et enregistrement des secrets du fichier .env dans Vault..."
# while IFS='=' read -r key value; do
# 	if [[ "$key" == \#* || "$key" == "" ]]; then
# 		continue
# 	fi

# 	key=$(echo $key | xargs)
# 	value=$(echo $value | xargs)

# 	echo "Enregistrement du secret pour la clé $key..."
# 	response=$(curl --silent --header "X-Vault-Token: $VAULT_TOKEN" \
# 					--request POST \
# 					--data "{\"data\": {\"$key\": \"$value\"}}" \
# 					$VAULT_ADDR/v1/kv/data/myapp/$key)

# 	echo "Réponse de Vault pour la clé $key: $response"

# 	echo $response | grep "errors" > /dev/null
# 	if [ $? -eq 0 ]; then
# 		echo "Erreur lors de l'enregistrement du secret pour la clé $key"
# 	fi
# done < "$ENV_FILE"

# echo "All secrets have been saved in Vault."

# # Get the list of secrets
# docker exec vault vault kv list kv/data/myapp
# echo "Vault initialization completed successfully."