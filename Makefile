.PHONY: help build up down restart logs logs-frontend logs-backend clean shell-frontend shell-backend test init-db health monitor ps
.PHONY: dev prod rebuild reset wait-healthy check-connections validate diagnose stats prune seed-db reset-db test-frontend test-backend test-integration

# Default target - show help
.DEFAULT_GOAL := help

# Enable BuildKit for faster builds and better caching
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ Basic Commands

help: ## Display this help message
	@echo "$(BLUE)VibeGraph Docker Management$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(YELLOW)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

build: ## Build all Docker images
	@echo "$(BLUE)Building all Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)Build complete!$(NC)"

up: ## Start all containers
	@echo "$(BLUE)Starting all containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Containers started!$(NC)"
	@echo "$(YELLOW)Run 'make wait-healthy' to wait for health checks$(NC)"

down: ## Stop all containers
	@echo "$(BLUE)Stopping all containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)Containers stopped!$(NC)"

restart: ## Restart all containers
	@echo "$(BLUE)Restarting all containers...$(NC)"
	docker-compose restart
	@echo "$(GREEN)Containers restarted!$(NC)"

##@ Development Commands

dev: ## Start containers in development mode with hot reload
	@echo "$(BLUE)Starting containers in development mode...$(NC)"
	docker-compose up --build
	@echo "$(GREEN)Development mode started!$(NC)"

prod: ## Start containers in production mode
	@echo "$(BLUE)Starting containers in production mode...$(NC)"
	docker-compose -f docker-compose.yml up -d --build
	@echo "$(GREEN)Production mode started!$(NC)"

rebuild: ## Clean and rebuild all images without cache
	@echo "$(BLUE)Rebuilding all images without cache...$(NC)"
	docker-compose build --no-cache
	@echo "$(GREEN)Rebuild complete!$(NC)"

reset: ## Stop containers, clean volumes, rebuild, and start fresh
	@echo "$(BLUE)Resetting entire environment...$(NC)"
	$(MAKE) down
	$(MAKE) clean
	$(MAKE) build
	$(MAKE) up
	@echo "$(YELLOW)Waiting for containers to be healthy...$(NC)"
	$(MAKE) wait-healthy
	$(MAKE) init-db
	@echo "$(GREEN)Environment reset complete!$(NC)"

##@ Logging Commands

logs: ## View logs from all containers
	@echo "$(BLUE)Viewing logs from all containers (Ctrl+C to exit)...$(NC)"
	docker-compose logs -f

logs-frontend: ## View frontend logs only
	@echo "$(BLUE)Viewing frontend logs (Ctrl+C to exit)...$(NC)"
	docker-compose logs -f frontend

logs-backend: ## View backend logs only
	@echo "$(BLUE)Viewing backend API logs (Ctrl+C to exit)...$(NC)"
	docker-compose logs -f backend-api

##@ Shell Access Commands

shell-frontend: ## Open shell in frontend container
	@echo "$(BLUE)Opening shell in frontend container...$(NC)"
	docker-compose exec frontend sh

shell-backend: ## Open shell in backend container
	@echo "$(BLUE)Opening shell in backend-api container...$(NC)"
	docker-compose exec backend-api sh

##@ Health Check Commands

health: ## Check health of all containers
	@echo "$(BLUE)Checking health of all containers...$(NC)"
	@docker-compose ps
	@echo ""
	@if docker-compose ps | grep -q "unhealthy"; then \
		echo "$(RED)Some containers are unhealthy!$(NC)"; \
		exit 1; \
	else \
		echo "$(GREEN)All containers are healthy!$(NC)"; \
	fi

wait-healthy: ## Wait for all containers to be healthy (timeout 120s)
	@echo "$(BLUE)Waiting for containers to be healthy...$(NC)"
	@timeout=120; \
	elapsed=0; \
	while [ $$elapsed -lt $$timeout ]; do \
		if docker-compose ps | grep -q "unhealthy\|starting"; then \
			echo "$(YELLOW)Waiting... ($$elapsed/$$timeout seconds)$(NC)"; \
			sleep 5; \
			elapsed=$$((elapsed + 5)); \
		else \
			echo "$(GREEN)All containers are healthy!$(NC)"; \
			exit 0; \
		fi; \
	done; \
	echo "$(RED)Timeout waiting for containers to be healthy$(NC)"; \
	docker-compose ps; \
	exit 1

monitor: ## Continuously monitor health status with comprehensive dashboard
	@echo "$(BLUE)Starting health monitoring dashboard...$(NC)"
	@./scripts/monitor-health.sh

ps: ## Show container status with health checks
	@echo "$(BLUE)Container Status:$(NC)"
	@docker-compose ps

##@ Database Commands

init-db: ## Initialize DynamoDB tables
	@echo "$(BLUE)Initializing DynamoDB tables...$(NC)"
	@echo "$(YELLOW)Waiting for DynamoDB to be ready...$(NC)"
	@sleep 5
	docker-compose run --rm dynamodb-init
	@echo "$(GREEN)Database initialized!$(NC)"

seed-db: ## Seed database with sample data
	@echo "$(BLUE)Seeding database with sample data...$(NC)"
	docker-compose exec backend-api python /app/scripts/seed-data.py
	@echo "$(GREEN)Database seeded!$(NC)"

reset-db: ## Reset database (delete all data)
	@echo "$(RED)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Resetting database...$(NC)"; \
		docker-compose down -v; \
		docker volume rm vibegraph-dynamodb-data 2>/dev/null || true; \
		$(MAKE) up; \
		$(MAKE) wait-healthy; \
		$(MAKE) init-db; \
		echo "$(GREEN)Database reset complete!$(NC)"; \
	else \
		echo "$(YELLOW)Database reset cancelled.$(NC)"; \
	fi

##@ Testing Commands

test: ## Run all tests (backend unit + frontend unit + integration)
	@echo "$(BLUE)Running all tests...$(NC)"
	@$(MAKE) test-backend
	@$(MAKE) test-frontend
	@$(MAKE) test-integration
	@echo "$(GREEN)All tests complete!$(NC)"

test-backend: ## Run backend unit tests with coverage
	@echo "$(BLUE)Running backend unit tests...$(NC)"
	docker-compose exec -T backend-api pytest tests/unit/ -v --cov=src --cov=api --cov-report=term-missing
	@echo "$(GREEN)Backend tests complete!$(NC)"

test-frontend: ## Run frontend unit tests with coverage
	@echo "$(BLUE)Running frontend unit tests...$(NC)"
	docker-compose exec -T frontend npm run test:coverage
	@echo "$(GREEN)Frontend tests complete!$(NC)"

test-integration: ## Run integration tests (end-to-end flows)
	@echo "$(BLUE)Running integration tests...$(NC)"
	@echo "$(YELLOW)Ensuring services are healthy...$(NC)"
	@$(MAKE) wait-healthy
	pytest tests/integration/ -v
	@echo "$(GREEN)Integration tests complete!$(NC)"

test-watch-backend: ## Run backend tests in watch mode
	@echo "$(BLUE)Running backend tests in watch mode...$(NC)"
	docker-compose exec backend-api pytest-watch tests/

test-watch-frontend: ## Run frontend tests in watch mode
	@echo "$(BLUE)Running frontend tests in watch mode...$(NC)"
	docker-compose exec frontend npm run test:watch

##@ Validation Commands

check-connections: ## Verify all inter-service connections
	@echo "$(BLUE)Checking inter-service connections...$(NC)"
	@echo "$(YELLOW)Checking backend-api → dynamodb-local...$(NC)"
	@docker-compose exec -T backend-api curl -sf http://dynamodb-local:8000 > /dev/null && \
		echo "$(GREEN)✓ DynamoDB connection OK$(NC)" || \
		echo "$(RED)✗ DynamoDB connection FAILED$(NC)"
	@echo "$(YELLOW)Checking backend-api → localstack...$(NC)"
	@docker-compose exec -T backend-api curl -sf http://localstack:4566/_localstack/health > /dev/null && \
		echo "$(GREEN)✓ LocalStack connection OK$(NC)" || \
		echo "$(RED)✗ LocalStack connection FAILED$(NC)"
	@echo "$(YELLOW)Checking backend-api health endpoint...$(NC)"
	@curl -sf http://localhost:8000/health > /dev/null && \
		echo "$(GREEN)✓ Backend API health OK$(NC)" || \
		echo "$(RED)✗ Backend API health FAILED$(NC)"
	@echo "$(YELLOW)Checking frontend...$(NC)"
	@curl -sf http://localhost:3000 > /dev/null && \
		echo "$(GREEN)✓ Frontend OK$(NC)" || \
		echo "$(RED)✗ Frontend FAILED$(NC)"
	@echo "$(GREEN)Connection checks complete!$(NC)"

validate: ## Run health checks and connection tests
	@echo "$(BLUE)Running validation checks...$(NC)"
	$(MAKE) health
	$(MAKE) check-connections
	@echo "$(GREEN)Validation complete!$(NC)"

diagnose: ## Run diagnostic checks and output detailed status
	@echo "$(BLUE)=== Diagnostic Report ===$(NC)"
	@echo ""
	@echo "$(YELLOW)Container Status:$(NC)"
	@docker-compose ps
	@echo ""
	@echo "$(YELLOW)Network Configuration:$(NC)"
	@docker network inspect vibegraph-network --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}' || echo "Network not found"
	@echo ""
	@echo "$(YELLOW)Volume Information:$(NC)"
	@docker volume ls | grep vibegraph || echo "No volumes found"
	@echo ""
	@echo "$(YELLOW)Resource Usage:$(NC)"
	@docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" $$(docker-compose ps -q) 2>/dev/null || echo "No containers running"
	@echo ""
	@echo "$(YELLOW)Recent Logs (last 20 lines):$(NC)"
	@docker-compose logs --tail=20
	@echo ""
	@echo "$(GREEN)Diagnostic report complete!$(NC)"

##@ Cleanup Commands

clean: ## Remove all containers, volumes, and images
	@echo "$(RED)WARNING: This will remove all containers, volumes, and images!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Cleaning up...$(NC)"; \
		docker-compose down -v --rmi all; \
		docker volume prune -f; \
		echo "$(GREEN)Cleanup complete!$(NC)"; \
	else \
		echo "$(YELLOW)Cleanup cancelled.$(NC)"; \
	fi

prune: ## Remove unused Docker resources
	@echo "$(BLUE)Pruning unused Docker resources...$(NC)"
	docker system prune -a --volumes -f
	@echo "$(GREEN)Prune complete!$(NC)"

##@ Advanced Commands

stats: ## View real-time resource usage
	@echo "$(BLUE)Viewing real-time resource usage (Ctrl+C to exit)...$(NC)"
	docker stats $$(docker-compose ps -q)


##@ Image Optimization Commands

image-sizes: ## Show Docker image sizes
	@echo "$(BLUE)Docker Image Sizes:$(NC)"
	@echo ""
	@docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "(REPOSITORY|vibegraph)" || echo "No vibegraph images found"
	@echo ""
	@echo "$(YELLOW)Total size of vibegraph images:$(NC)"
	@docker images --format "{{.Size}}" | grep -E "vibegraph" | awk '{sum += $1} END {print sum " MB"}' || echo "0 MB"

build-info: ## Show build information and optimization status
	@echo "$(BLUE)Build Configuration:$(NC)"
	@echo "DOCKER_BUILDKIT: $(DOCKER_BUILDKIT)"
	@echo "COMPOSE_DOCKER_CLI_BUILD: $(COMPOSE_DOCKER_CLI_BUILD)"
	@echo ""
	@echo "$(BLUE)BuildKit Status:$(NC)"
	@docker buildx version 2>/dev/null && echo "$(GREEN)✓ BuildKit available$(NC)" || echo "$(RED)✗ BuildKit not available$(NC)"
	@echo ""
	@$(MAKE) image-sizes

build-frontend: ## Build only frontend image
	@echo "$(BLUE)Building frontend image...$(NC)"
	docker-compose build frontend
	@echo "$(GREEN)Frontend build complete!$(NC)"

build-backend: ## Build only backend images
	@echo "$(BLUE)Building backend images...$(NC)"
	docker-compose build backend-api backend-handlers backend-services
	@echo "$(GREEN)Backend build complete!$(NC)"

inspect-layers: ## Inspect Docker image layers (usage: make inspect-layers IMAGE=vibegraph-frontend)
	@if [ -z "$(IMAGE)" ]; then \
		echo "$(RED)Error: IMAGE parameter required$(NC)"; \
		echo "Usage: make inspect-layers IMAGE=vibegraph-frontend"; \
		exit 1; \
	fi
	@echo "$(BLUE)Inspecting layers for $(IMAGE)...$(NC)"
	@docker history $(IMAGE) --human --no-trunc
