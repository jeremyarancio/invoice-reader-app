.PHONY: *

#----Prod----
prod-up:
	@echo "Starting production environment..."
	docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d
	@echo "Invoice Manager running!"

prod-logs:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod logs -f $(SERVICE)

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

#----Version Management----
version-current:
	@echo "Current version: $$(cat VERSION)"

version-bump-patch:
	@echo "Bumping patch version..."
	@uvx --with commitizen cz bump --increment PATCH

version-bump-minor:
	@echo "Bumping minor version..."
	@uvx --with commitizen cz bump --increment MINOR

version-bump-major:
	@echo "Bumping major version..."
	@uvx --with commitizen cz bump --increment MAJOR

version-tag:
	@echo "Creating git tag for version $$(cat VERSION)..."
	git tag -a "v$$(cat VERSION)" -m "Release version $$(cat VERSION)"
	@echo "Tag created. Push with: git push origin v$$(cat VERSION)"