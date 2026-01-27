.PHONY: help up down logs shell-db restart clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start PostgreSQL and Redis containers
	docker-compose -f docker/docker-compose.yml up -d
	@echo "Waiting for services to be ready..."
	@sleep 3
	@echo "Services started. Use 'make logs' to view logs."

down: ## Stop and remove containers
	docker-compose -f docker/docker-compose.yml down

logs: ## View logs from all services
	docker-compose -f docker/docker-compose.yml logs -f

shell-db: ## Open PostgreSQL shell
	docker exec -it lifestream-postgres psql -U lifestream -d lifestream

restart: ## Restart all services
	docker-compose -f docker/docker-compose.yml restart

clean: ## Stop containers and remove volumes (WARNING: deletes data)
	docker-compose -f docker/docker-compose.yml down -v
	@echo "All containers and volumes removed."
