.PHONY: *

dev-ui:
	cd ui/ && npm run dev

dev-server:
	uv run --directory src/ fastapi dev invoice_reader/app/routes.py

format:
	uv tool run ruff format .

lint:
	uv tool run ruff check --fix

fix: lint format

