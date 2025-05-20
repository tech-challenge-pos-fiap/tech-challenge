# tech-challenge

## Stacks
- Python
- FastAPI
- PostgreSQL
- Alembic
- SQLAlchemy

## Requisitos
- Docker

## Iniciando o projeto
```sh
docker compose up
```

## Gerenciamento de Migrations com Makefile

Para facilitar o uso do Alembic via Docker, utilize os comandos abaixo:

### Criar uma nova migration

```sh
make migration name="nome_da_migration"
```
Exemplo:
```sh
make migration name="add_tabela_pagamento"
```

### Executar todas as migrations pendentes

```sh
make migrate
```
