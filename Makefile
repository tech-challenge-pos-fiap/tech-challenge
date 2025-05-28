# Makefile para facilitar comandos do Alembic via Docker

# Nome do container do serviço FastAPI
CONTAINER=fastapi

# Cria uma nova migration (exemplo de uso: make migration name="add_nova_tabela")
migration:
	docker compose run --rm $(CONTAINER) alembic revision --autogenerate -m "$(name)"

# Executa todas as migrations pendentes
migrate:
	docker compose run --rm $(CONTAINER) alembic upgrade head
