all:
	./get_ip_in_env.sh
	docker compose up -d --build
	@./display_ip.sh

# Build the Docker images using docker compose
build:
	docker compose build

# Start the services in detached mode
up:
	docker compose up -d

# Stop the services
down:
	docker compose down

# Clean up Docker containers, images, volumes, and networks
clean:
	docker compose down --rmi all --volumes --remove-orphans

# Clean up Vault-related files and directories
cleanfiles:
	@read -p "Are you sure you want to delete Vault logs, data, policies, and key files? (y/N) " confirm && \
	[ "$$confirm" = "y" ] || exit 1
	rm -rf ./vault/logs ./vault/data
	rm -f ./vault/config/init.file \
	      ./vault/config/root.token \
	      ./vault/config/unseal.key1 \
	      ./vault/config/unseal.key2 \
	      ./vault/config/unseal.key3 \
	      ./vault/config/unseal.key4 \
	      ./vault/config/unseal.key5
	@echo "✅ Vault files and directories have been cleaned."

# Fully clean up all Docker resources
dockerfclean:
	# Stop all running containers and remove all containers
	docker container stop $$(docker container ls -aq) || true
	docker container rm $$(docker container ls -aq) || true

	# Remove all images
	docker image prune -a -f

	# Remove all volumes
	docker volume prune -f

	# Remove all networks
	docker network prune -f

	# Remove all build cache
	docker builder prune -a -f

	# Remove unused Docker objects
	docker system prune -a -f --volumes

	@echo "✅ Docker system has been fully cleaned."


# A combined clean target that includes both Docker and Vault cleanup
fclean: clean cleanfiles dockerfclean
	@echo "✅ Full cleanup completed."

# Verbose mode
v:
	$(MAKE) --no-print-directory MAKEFLAGS="-n" all

# Declare phony targets to avoid conflicts with files of the same name
.PHONY: build up down clean cleanfiles