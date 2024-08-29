#! /bin/bash

until curl -k --silent -u elastic:${ELASTIC_PASSWORD} https://localhost:9200/_cluster/health?wait_for_status=yellow | grep -q '"status":"yellow"'; do
    echo "Attente de l'initialisation d'Elasticsearch..."
    sleep 10
done

# Générer un token API
API_RESPONSE=$(curl -k -u elastic:${ELASTIC_PASSWORD} -X POST "https://localhost:9200/_security/api_key" -H 'Content-Type: application/json' -d'
{
  "name": "my_api_key",
  "role_descriptors": {
    "my_role": {
      "cluster": ["all"],
      "index": [
        {
          "names": ["*"],
          "privileges": ["read"]
        }
      ]
    }
  }
}
')

# Extraire le token API de la réponse JSON
API_KEY=$(echo $API_RESPONSE | jq -r '.api_key')

if [ -z "$API_KEY" ]; then
    echo "Erreur lors de la génération du token API"
    exit 1
fi

echo "Token API généré avec succès : $API_KEY"

# Optionnel : Configurer Kibana pour utiliser ce token (si besoin)
# Par exemple, tu peux l'écrire dans un fichier de configuration, ou l'utiliser directement dans un autre script
echo "API_KEY=${API_KEY}" > api_key.env

echo "Configuration terminée."