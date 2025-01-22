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