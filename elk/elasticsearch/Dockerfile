FROM docker.elastic.co/elasticsearch/elasticsearch:8.4.0
RUN mkdir -p /usr/share/elasticsearch/config/certs

RUN /usr/share/elasticsearch/bin/elasticsearch-certutil cert --self-signed --out /usr/share/elasticsearch/config/certs/elastic-certificates.p12 --pass ""