#!/bin/bash

# Verbose mode: on
set -x

# Start Vault in server mode with the specified configuration
echo "Starting Vault server with configuration..."
vault server -config=vault-config.hcl -tls-skip-verify &
VAULT_PID=$!
echo "Vault server started with PID $VAULT_PID."

# Wait for Vault to start
echo "Waiting for Vault server to start..."
sleep 5

# Initialize Vault if not already initialized
if [ ! -f /vault/config/init.file ]; then
    echo "Initializing Vault..."
    init_output=$(vault operator init -key-shares=5 -key-threshold=3 -tls-skip-verify)
    
    if [ $? -ne 0 ]; then
        echo "Vault initialization failed."
        exit 1
    fi

    echo "$init_output" > /vault/config/init.file
	echo "Vault initialization complete. Saving unseal keys and root token..."

    for i in {1..5}; do
        cat /vault/config/init.file | grep "Unseal Key $i:" | awk '{print $NF}' > "/vault/config/unseal.key$i"
    done

    cat /vault/config/init.file | grep 'Initial Root Token:' | awk '{print $NF}' > /vault/config/root.token
    echo "Vault initialized and keys saved."
else
    echo "Vault is already initialized. Skipping initialization."
fi

# Unseal Vault using 3 random unseal keys out of the 5
echo "Unsealing Vault with 3 random keys..."
shuf -n 3 -e /vault/config/unseal.key{1..5} | while read keyfile; do
    vault operator unseal -tls-skip-verify $(cat "$keyfile")
done

# Check if unsealing was successful
if [ $? -ne 0 ]; then
    echo "Unsealing Vault failed."
    exit 1
else
    echo "Vault unsealed successfully."
fi

# Log in using the root token
echo "Logging in to Vault with the root token..."
vault login -tls-skip-verify $(cat /vault/config/root.token)

# Check if login was successful
if [ $? -ne 0 ]; then
    echo "Vault login failed."
    exit 1
else
    echo "Logged in to Vault successfully."
fi

# Export the root token as an environment variable
export VAULT_TOKEN=$(cat /vault/config/root.token)


# Enable the KV secrets engine at the path "secret"
echo "Enabling KV secrets engine..."
vault secrets enable -path=secret kv -tlss-skip-verify

if [ $? -ne 0 ]; then
    echo "Failed to enable KV secrets engine."
    exit 1
else
    echo "KV secrets engine enabled successfully."
fi

# Load environment variables from a .env file into Vault
ENV_FILE=/vault/config/.env

if [ -f "$ENV_FILE" ]; then
    echo "Loading secrets from .env file..."
    while IFS='=' read -r key value; do
        if [[ "$key" == \#* || "$key" == "" ]]; then
            continue
        fi
        key=$(echo $key | xargs)
        value=$(echo $value | xargs)
        echo "Storing secret $key..."
        vault kv put secret/myapp/$key value=$value -tls-skip-verify
    done < "$ENV_FILE"
    echo "All secrets have been saved in Vault."
else
    echo "No .env file found. Skipping secret loading."
fi

# Wait for Vault process to finish
echo "Vault server is running. Waiting for process to finish..."
wait $VAULT_PID



# VAULT_ADDR="http://0.0.0.0:8200"

# echo "Initializing Vault... $VAULT_ADDR"


# # Check if vault is already initialized
# init_output=$(docker exec vault vault operator init)
# if [ $? -ne 0 ]; then
# 	ec -tls-skip-verifyho "[ERROR] Vault initialization failed"
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