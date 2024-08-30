#!/bin/bash

# Utilisation de la variable d'environnement ELASTIC_PWD
echo "Le mot de passe Elasticsearch est: ${ELASTIC_PWD}"

# Exécution de la commande Elasticsearch avec les configurations nécessaires
# exec elasticsearch