.PHONY: *

dev-ui:
	cd ui/ && npm run dev

dev-server:
	uv run --directory src/ fastapi dev invoice_reader/app/routes.py