SHELL := /bin/sh

BACKEND_DIR := backend
FRONTEND_DIR := frontend
FRONTEND_VENV := $(FRONTEND_DIR)/.venv
FRONTEND_PYTHON := $(FRONTEND_VENV)/bin/python
FRONTEND_REFLEX := $(FRONTEND_VENV)/bin/reflex

API_URL ?= http://localhost:8000
FRONTEND_PORT ?= 3000
REFLEX_BACKEND_PORT ?= 8002

.DEFAULT_GOAL := help
.NOTPARALLEL:

.PHONY: help setup env up logs down backend-up backend-logs backend-down restart status wait-db migrate frontend-install frontend-run frontend-compile db-shell api-shell

help: ## Lista os comandos disponiveis
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: env frontend-install ## Prepara .env do backend e venv do frontend

env: ## Cria backend/.env se ainda nao existir
	@if [ ! -f "$(BACKEND_DIR)/.env" ]; then \
		printf '%s\n' 'DATABASE_URL=postgresql://postgres:postgres@db:5432/inscricoes_db' > "$(BACKEND_DIR)/.env"; \
		echo "Criado $(BACKEND_DIR)/.env"; \
	else \
		echo "$(BACKEND_DIR)/.env ja existe"; \
	fi

up: migrate frontend-install ## Sobe API, banco, migrations e frontend
	cd $(FRONTEND_DIR) && INSCRICOES_API_URL=$(API_URL) ./.venv/bin/reflex run --frontend-port $(FRONTEND_PORT) --backend-port $(REFLEX_BACKEND_PORT)

logs: backend-logs ## Mostra logs da API e do banco

down: backend-down ## Para API e banco

backend-up: env ## Sobe API e banco em background
	cd $(BACKEND_DIR) && docker compose up --build -d

backend-logs: ## Mostra logs da API e do banco
	cd $(BACKEND_DIR) && docker compose logs -f

backend-down: ## Para API e banco
	cd $(BACKEND_DIR) && docker compose down

restart: backend-down backend-up migrate ## Reinicia API e banco, depois roda migrations

status: ## Mostra status dos containers
	cd $(BACKEND_DIR) && docker compose ps

wait-db: backend-up ## Aguarda o PostgreSQL aceitar conexoes
	@echo "Aguardando banco..."
	@cd $(BACKEND_DIR) && i=0; \
	until docker compose exec -T db pg_isready -U postgres -d inscricoes_db >/dev/null 2>&1; do \
		i=$$((i + 1)); \
		if [ $$i -ge 30 ]; then \
			echo "Banco nao ficou pronto em ate 30 segundos."; \
			exit 1; \
		fi; \
		sleep 1; \
	done

migrate: wait-db ## Aplica migrations pendentes
	cd $(BACKEND_DIR) && docker compose exec -T api alembic upgrade head

$(FRONTEND_REFLEX): $(FRONTEND_DIR)/requirements.txt
	python3 -m venv $(FRONTEND_VENV)
	$(FRONTEND_PYTHON) -m pip install --upgrade pip
	$(FRONTEND_PYTHON) -m pip install -r $(FRONTEND_DIR)/requirements.txt

frontend-install: $(FRONTEND_REFLEX) ## Instala dependencias do frontend

frontend-run: frontend-install ## Sobe o frontend Reflex em foreground
	cd $(FRONTEND_DIR) && INSCRICOES_API_URL=$(API_URL) ./.venv/bin/reflex run --frontend-port $(FRONTEND_PORT) --backend-port $(REFLEX_BACKEND_PORT)

frontend-compile: frontend-install ## Compila o frontend sem subir servidor
	cd $(FRONTEND_DIR) && ./.venv/bin/reflex compile

db-shell: wait-db ## Abre o psql no banco local
	cd $(BACKEND_DIR) && docker compose exec db psql -U postgres -d inscricoes_db

api-shell: backend-up ## Abre um shell no container da API
	cd $(BACKEND_DIR) && docker compose exec api sh
