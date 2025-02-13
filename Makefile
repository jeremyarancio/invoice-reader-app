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

# Docker
dev:
	docker-compose --env-file ./server/.env up -d

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

tag: tag-server tag-ui tag-pg

tag-server:
	docker tag invoice-server:latest 265890761777.dkr.ecr.eu-central-1.amazonaws.com/invoice-server

tag-ui:
	docker tag invoice-ui:latest 265890761777.dkr.ecr.eu-central-1.amazonaws.com/invoice-ui

tag-pg:
	docker tag postgres:17.2-alpine 265890761777.dkr.ecr.eu-central-1.amazonaws.com/invoice-postgres

push: push-server push-ui push-pg

push-server:
	docker push 265890761777.dkr.ecr.eu-central-1.amazonaws.com/invoice-server

push-ui:
	docker push 265890761777.dkr.ecr.eu-central-1.amazonaws.com/invoice-ui

push-pg:
	docker push 265890761777.dkr.ecr.eu-central-1.amazonaws.com/invoice-postgres

# Terraform
apply:
	terraform -chdir=infra apply

destroy:
	terraform -chdir=infra destroy