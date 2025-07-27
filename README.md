# 🍔 Tech Challenge - Sistema de Autoatendimento para Fast Food

## 💡 Sobre o Projeto

Este projeto faz parte do **Tech Challenge - Fase 1** da **Pós-Tech em Software Architecture** da **FIAP**.

O objetivo é desenvolver um **sistema de autoatendimento para uma lanchonete em expansão**, resolvendo problemas relacionados ao controle de pedidos, preparo e entrega. O projeto busca aumentar a eficiência do atendimento ao cliente e garantir a confiabilidade dos pedidos.

## 🧰 Stacks Utilizadas
- Python
- FastAPI
- PostgreSQL
- Alembic
- SQLAlchemy

## 🧱 Pré-requisitos
- Docker

## 🚀 Como Iniciar o Projeto
Clone o repositório:
```sh
git clone https://github.com/tech-challenge-pos-fiap/tech-challenge.git
cd tech-challenge
```
Construa a imagem Docker:
```sh
make build
```

Rode as migrations do Alembic:
```sh
make migrate
```

Suba o container:
```sh
make up
```
O arquivo **Makefile** possui alguns outros comandos úteis para o projeto.

Com o container rodando, você pode acessar a documentação da API através da URL:
```url
localhost:8000/docs
```

## 🏛 Arquitetura Hexagonal

O projeto adota a Arquitetura Hexagonal para garantir uma separação clara entre a lógica de negócio e os detalhes de infraestrutura, como banco de dados e interfaces HTTP.
Isso permite que a aplicação seja mais fácil de testar, manter e evoluir, além de tornar possível trocar tecnologias externas sem impactar o núcleo da aplicação.


## 🗂️ Estrutura de Pastas


- `alembic/`
  - Migrations do banco gerenciadas pelo Alembic.

- `app/`
  - Diretório principal da aplicação.

  - `domain/`
    - Contém a lógica de negócio.
    - `models/`: Entidades principais do domínio.
    - `value_objects/`: Objetos de valor imutáveis.

  - `application/`
    - Casos de uso da aplicação.
    - `ports/`: Interfaces que descrevem contratos com adaptadores.
    - `services/`: Serviços que coordenam lógica de negócio.

  - `adapters/`
    - Adaptadores de entrada e saída do sistema.

    - `api/`
      - `routes/`: Endpoints HTTP.
      - `dtos/`: Objetos de entrada/saída via API.

    - `persistence/`
      - `models/`: Modelos ORM do banco de dados.
      - `repositories/`: Implementações dos repositórios.

    - `external/`
      - Integrações com sistemas externos (ex: Mercado Pago).

  - `config/`
    - Configurações da aplicação (ex: banco de dados, envs).

- `tests/`
  - Testes automatizados.

### 🧭 Mapa Visual

```
.
├── alembic/
├── app/
│   ├── domain/
│   │   ├── models
│   │   └── value_objects
│   ├── application/
│   │   ├── ports
│   │   └── services
│   ├── adapters/
│   │   ├── api/
│   │   │   ├── routes
│   │   │   └── dtos
│   │   ├── persistence/
│   │   │   ├── models
│   │   │   └── repositories
│   │   └── external
│   └── config
└── tests/
```
