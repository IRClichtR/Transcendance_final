FROM docker.elastic.co/elastic.co/kibana/kibana:8.4.0

RUN apt-get update && apt-get install -y openssl

RUN mkdir -p /usr/share/kibana/config/certs 

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /usr/share/kibana/config/certs/kibana.key \
    -out /usr/share/kibana/config/certs/kibana.crt \
    -subj "/CN=localhost"

# Copier le script de configuration dans le conteneur
COPY setup_elasticsearch.sh /usr/local/bin/setup_elasticsearch.sh

# Rendre le script exécutable
RUN chmod +x /usr/local/bin/setup_elasticsearch.sh

# Ajouter une commande pour exécuter le script lors du démarrage du conteneur
CMD ["/bin/bash", "-c", "/usr/local/bin/setup_elasticsearch.sh && /usr/local/bin/kibana-docker"]