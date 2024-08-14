#!/bin/bash

# Extraire l'adresse IP du fichier .env
IP=$(grep -oP '^HOST_IP=\K.*' .env)

# Afficher le message avec l'adresse IP
echo ""
echo "Your website is available at: https://${IP}:8443"
