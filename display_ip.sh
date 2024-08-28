#!/bin/bash
OS=$(uname)
# Extraire l'adresse IP du fichier .env
if [ "$OS" == "Darwin" ]; then
    IP=$(grep '^HOST_IP=' .env | cut -d '=' -f 2)
else
	IP=$(grep -oP '^HOST_IP=\K.*' .env)
fi
# Afficher le message avec l'adresse IP
echo ""
echo "Your website is available at: https://${IP}:8443"
