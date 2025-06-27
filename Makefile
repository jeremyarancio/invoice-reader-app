.PHONY: *

#----Local dev without Docker----
dev-ui:
	cd ui/ && npm run dev

dev-server:
	cd server/ && uv run --directory src/ fastapi dev invoice_reader/app/main.py

#----Formating----
fix: lint format

format:
	cd server && uv tool run ruff format .

lint:
	cd server && uv tool run ruff check --fix


test:
	cd server && uv run pytest -vv

#----Docker----
compose-up:
	docker compose up -d

compose-build:
	docker compose up -d --build

logs:
	docker compose logs -f

down:
	docker compose down

build: build-server build-ui build-pg

# We take the prod stage for production
build-server:
	docker build -t invoice-server --target prod ./server

build-ui:
	docker build -t invoice-ui ./ui

build-pg:
	docker build -t postgres:17.2-alpine