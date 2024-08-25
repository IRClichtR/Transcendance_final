#!/bin/bash

/usr/share/elasticsearch/bin/elasticsearch &

echo "Waiting for Elasticsearch to start..."
while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" -XGET 'http://localhost:9200')
    if [[ "$response" == "200" || "$response" == "401" ]]; then
        break
    fi
    sleep 5
done

echo "Resetting password for built-in user 'elastic'..."
new_password=$(< /dev/urandom tr -dc A-Za-z0-9 | head -c20) # Générer un mot de passe aléatoire
echo "New password: $new_password"
/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic -p "$new_password" -i --batch

# Vérifier que le mot de passe a bien été récupéré
echo "----- DEBUG -----"
echo "elastic_password=$new_password"
echo "-----------------"

# echo "Setting up passwords for built-in users..."
# /usr/share/elasticsearch/bin/elasticsearch-setup-passwords auto --batch > /usr/share/elasticsearch/config/setup-passwords.log 2>&1
#
# echo "----- DEBUG -----"
# cat /usr/share/elasticsearch/config/setup-passwords.log
# echo "-----------------"
# # Récupérer le mot de passe généré pour l'utilisateur elastic
# elastic_password=$(grep 'PASSWORD elastic =' /usr/share/elasticsearch/config/setup-passwords.log | awk '{print $4}')
#
# echo "----- DEBUG -----\nelastic_password= $elastic_password\n"

# Vérifier l'état du cluster en utilisant le mot de passe généré
echo "Verifying cluster health..."
until curl -u elastic:$new_password -sSf -XGET 'http://localhost:9200/_cluster/health?pretty' > /dev/null; do
    sleep 5
done

echo "Elasticsearch setup completed. Passwords are stored in /usr/share/elasticsearch/config/setup-passwords.log"

exec "$@"
