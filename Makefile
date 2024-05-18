build:
	docker compose build

down:
	docker compose stop && docker compose down

start:
	docker compose up

restart:
	docker compose restart api worker

up: build start migrate static

migrate:
	docker compose run --rm api python manage.py migrate

migrations:
	docker compose run --rm api python manage.py makemigrations

mm: migrations migrate

bash:
	docker compose run --rm api /bin/sh

admin:
	docker compose exec api python manage.py createsuperuser

app:
	docker compose exec api python3 manage.py startapp $(name) && mv $(name) apps/$(name)
