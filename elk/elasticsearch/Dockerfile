ARG REPOSITORY_BASE=docker.elastic.co

FROM ${REPOSITORY_BASE}/kibana/kibana:8.4.0
RUN mkdir -p /usr/share/elasticsearch/config/certs

RUN /usr/share/elasticsearch/bin/elasticsearch-certutil cert --out /usr/share/elasticsearch/config/certs/elastic-certificates.p12 --pass ""