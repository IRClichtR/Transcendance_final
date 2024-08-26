FROM postgres:16

WORKDIR /docker-entrypoint-initdb.d

COPY ./init-scripts /docker-entrypoint-initdb.d

CMD ["postgres"]