#!/bin/bash

# Charger les variables d'environnement depuis le fichier .env
export $(grep -v '^#' .env | xargs)

# Vérifier si la variable APP_IP est définie
if [ -z "$HOST_IP" ]; then
  echo "La variable HOST_IP n'est pas définie dans le fichier .env"
  exit 1
fi

# Générer la configuration Nginx
cat <<EOF > modsecurity-nginx/conf/default
upstream web {
    server web:8001;
}

upstream game {
    server game:8002;
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_certificate /etc/nginx/ssl/transcendance.crt;
    ssl_certificate_key /etc/nginx/ssl/transcendance.key;

    location / {
        proxy_pass http://web;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;

        add_header X-Content-Type-Options nosniff;
    }

    location /pong {
        proxy_pass http://game;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_redirect off;

        add_header X-Content-Type-Options nosniff;
    }

    location /ws/ {
        proxy_pass http://game;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate /etc/nginx/ssl/transcendance.crt;
    ssl_certificate_key /etc/nginx/ssl/transcendance.key;

    location / {
        return 301 https://$HOST_IP:8443\$request_uri;
    }
}
EOF
