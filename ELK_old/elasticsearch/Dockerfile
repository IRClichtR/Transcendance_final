FROM elasticsearch:8.12.0

COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
COPY tls-certificates/ /usr/share/elasticsearch/config
COPY credentials_gen.sh /usr/share/elasticsearch/config/credentials_gen

CMD /usr/share/elasticsearch/config/credentials_gen