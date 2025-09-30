.PHONY: *

#----Prod----
prod-up:
	@echo "Starting production environment..."
	docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d
	@echo "Invoice Manager running!"

prod-logs:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod logs -f

prod-down:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod down

#----Dev----
dev-up:
	docker compose up -d

dev-build:
	docker compose up -d --build

dev-logs:
	docker compose logs -f

dev-down:
	docker compose down