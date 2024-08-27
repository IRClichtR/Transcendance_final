all:
	./get_ip_in_env.sh
	docker compose up -d --build
	@./display_ip.sh

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