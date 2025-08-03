# Makefile para facilitar comandos do Alembic via Docker

# Nome do container do serviço FastAPI
CONTAINER=fastapi

# variables to kube setuo
KUBE_DIR := kube
APP_DIR := $(KUBE_DIR)/app
DB_DIR := $(KUBE_DIR)/db
SERVICE_NAME := api-service

# Cria uma nova migration (exemplo de uso: make migration name="add_nova_tabela")
migration:
	docker compose run --rm $(CONTAINER) alembic revision --autogenerate -m "$(name)"

# Executa todas as migrations pendentes
migrate:
	docker compose run --rm $(CONTAINER) alembic upgrade head

# Constrói a imagem
build:
	docker compose build

up:
	docker compose up

rebuild:
	docker compose down -v --remove-orphans
	docker compose build --no-cache

format:
	docker compose run --rm $(CONTAINER) ruff format

check:
	docker compose run --rm $(CONTAINER) ruff check

fix:
	docker compose run --rm $(CONTAINER) ruff check --fix

setup-kube:
	@echo "🚀 Starting Minikube (if not running)..."
	@minikube status >/dev/null 2>&1 || minikube start --cpus=4 --memory=4g --driver=docker
	@echo "📊 Enabling metrics-server addon..."
	minikube addons enable metrics-server
	@echo "📦 Applying DB manifests..."
	kubectl apply -f $(DB_DIR)
	@echo "🧩 Applying App manifests..."
	kubectl apply -f $(APP_DIR)
	@echo "🌐 Exposing service $(SERVICE_NAME)..."
	@minikube service $(SERVICE_NAME)
