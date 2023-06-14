SHELL=/bin/bash

setup:
	poetry lock --no-update
	poetry install

run_postgres:
	@if ! docker ps --format '{{.Names}}' | grep -q '^test_postgres$$'; then \
		docker run --name test_postgres \
			-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
			-e POSTGRES_DB=$(POSTGRES_DB) \
			-p $(POSTGRES_PORT):5432 -d postgres:latest; \
		echo "Waiting for PostgreSQL container to start..." && sleep 7; \
	else \
		echo "PostgreSQL container is already running"; \
	fi

server:
	set -a; source .env; set +a; poetry run python manage.py runserver $$HOST:$$PORT

analyze:
	poetry run mypy apps
	poetry run pylint apps

test: run_postgres
	set -a; source .env set +a; poetry run python manage.py test type_based_creator


