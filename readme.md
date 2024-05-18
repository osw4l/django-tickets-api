# Tickets Api

## System Requirements 

- Docker App https://www.docker.com/products/docker-desktop/
- Terminal (I'm using https://iterm2.com/)


## Commands for running

- tests: `cp env_template .env` and fill the secrets with yours
- run build and containers: `make up`
- check containers status: `docker compose ps`
- run migrations: `make migrate`
- create superuser : `make admin`

# Urls for access
- api docs: http://127.0.0.1:9600/ 

## I recommend you log in in the admin to interact with api docs

http://127.0.0.1:9600/admin/login/

## You can also interact once logged in with the rest framework browseable api

http://127.0.0.1:9600/tickets/tickets/

here you can

- create tickets
- view tickets
- list tickets and filter by created_at date and status
- upload photos to the tickets