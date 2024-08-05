#
#OMPOSE_FILE = ./docker-compose.yml

all:
	./get_ip_in_env.sh
	./modsecurity-nginx/generate_nginx_config.sh
	docker compose up -d --build

d:
	docker compose down -v

pong:
	./get_ip_in_env.sh
	docker compose up -d --build

clean: d
	docker rmi $(shell docker images -q)

prune: d clean
	docker builder prune -f
	docker system prune -f


.PHONY: pong
