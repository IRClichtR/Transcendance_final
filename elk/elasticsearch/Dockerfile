FROM docker.elastic.co/elasticsearch/elasticsearch:8.4.0

USER root 
RUN apt-get update && apt-get install openssl -y
RUN openssl genpkey -algorithm RSA -out ca-key.pem -aes256 -pass pass:"1234"
RUN ls -la
RUN cat ca-key.pem
RUN openssl req -new -x509 -key ca-key.pem -out ca-cert.pem -days 365 -passin pass:"1234" -subj "/C=US/ST=State/L=City/O=transcendance/OU=elk/CN=commonname"

RUN openssl genpkey -algorithm RSA -out elastic-key.pem
RUN ls -la
RUN cat elastic-key.pem
RUN openssl req -new -x509 -key elastic-key.pem -out elastic-cert.pem -days 365 -subj "/C=US/ST=State/L=City/O=transcendance/OU=elk/CN=commonname"

RUN mkdir -p /usr/share/elasticsearch/config/certs

RUN openssl pkcs12 -export -in elastic-cert.pem -inkey elastic-key.pem -certfile ca-cert.pem -out /usr/share/elasticsearch/config/certs/elastic-certificates.p12 -name "elasticsearch" -passout pass:"1234"
# RUN ls -la /usr/share/elasticsearch/config/certs
RUN openssl pkcs12 -info -in /usr/share/elasticsearch/config/certs/elastic-certificates.p12 -noout -password pass:"1234"
RUN chown elasticsearch:elasticsearch /usr/share/elasticsearch/config/certs/elastic-certificates.p12
USER elasticsearch

# CMD ["/usr/local/bin/init.sh"]