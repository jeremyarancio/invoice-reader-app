.PHONY: *

dev-ui:
	cd ui/ && npm run dev

dev-server:
	cd server/ && uv run --directory src/ fastapi dev invoice_reader/app/routes.py

format:
	cd server && uv tool run ruff format .

lint:
	cd server && uv tool run ruff check --fix

fix: lint format

test:
	cd server && uv run pytest -vv

dev:
	docker-compose --env-file ./server/.env up -d

build:
	docker-compose --env-file ./server/.env up --build -d

logs:
	docker compose logs -f

down:
	docker compose down