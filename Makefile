SHELL=/bin/bash

setup:
	poetry lock --no-update
	poetry install

server:
	poetry run python manage.py runserver 0.0.0.0:8000