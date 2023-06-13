SHELL=/bin/bash

setup:
	poetry lock --no-update
	poetry install

server:
	set -a; source .env set +a; poetry run python manage.py runserver 0.0.0.0:8000