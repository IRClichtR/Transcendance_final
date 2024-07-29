#
#OMPOSE_FILE = ./docker-compose.yml

all:
	./get_ip_in_env.sh
	docker compose up -d --build
	docker compose exec server python backend_server/manage.py migrate --noinput
	docker compose exec server python backend_server/manage.py collectstatic --no-input --clear

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
