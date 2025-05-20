# Makefile para facilitar comandos do Alembic via Docker

# Nome do container do serviço FastAPI
CONTAINER=fastapi_server

# Cria uma nova migration (exemplo de uso: make migration name="add_nova_tabela")
migration:
	docker exec $(CONTAINER) alembic revision --autogenerate -m "$(name)"

# Executa todas as migrations pendentes
migrate:
	docker exec $(CONTAINER) alembic upgrade head 