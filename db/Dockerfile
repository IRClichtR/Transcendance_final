# Utiliser l'image officielle de PostgreSQL 16 comme base
FROM postgres:16

# Définir un répertoire de travail
WORKDIR /docker-entrypoint-initdb.d

# Copier les scripts d'initialisation dans le répertoire de travail
COPY ./init-scripts /docker-entrypoint-initdb.d

# Définir les variables d'environnement par défaut (vous pouvez les surcharger avec un fichier .env)
ENV POSTGRES_USER=basbarludflo
ENV POSTGRES_PASSWORD=qCJRUpuC78D9aK2gk7cJz7P
ENV POSTGRES_DB=transcendance_DB
ENV POSTGRES_DB2=pong_DB

# Exposer le port par défaut de PostgreSQL
EXPOSE 5432

# Définir la commande par défaut pour démarrer PostgreSQL
CMD ["postgres"]