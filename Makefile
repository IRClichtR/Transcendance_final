all:
	./get_ip_in_env.sh
	./modsecurity-nginx/generate_nginx_config.sh
	docker compose up -d --build
	@./display_ip.sh

# Build the Docker images using docker-compose
build:
	docker-compose build

# Start the services in detached mode
up:
	docker-compose up -d

# Stop the services
down:
	docker-compose down

# Clean up Docker containers, images, volumes, and networks
clean:
	docker-compose down --rmi all --volumes --remove-orphans

# Clean up Vault-related files and directories
cleanfiles:
	@read -p "Are you sure you want to delete Vault logs, data, policies, and key files? (y/N) " confirm && \
	[ "$$confirm" = "y" ] || exit 1
	rm -rf ./vault/logs ./vault/data ./vault/policies
	rm -f ./vault/config/init.file \
	      ./vault/config/root.token \
	      ./vault/config/unseal.key1 \
	      ./vault/config/unseal.key2 \
	      ./vault/config/unseal.key3 \
	      ./vault/config/unseal.key4 \
	      ./vault/config/unseal.key5
	@echo "✅ Vault files and directories have been cleaned."


# A combined clean target that includes both Docker and Vault cleanup
fclean: clean cleanfiles
	@echo "✅ Full cleanup completed."


# Declare phony targets to avoid conflicts with files of the same name
.PHONY: build up down clean cleanfiles