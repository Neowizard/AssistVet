.PHONY: debug start debug logs stop

up:
	docker compose up -d

debug:
	docker compose -f docker-compose-dev.yaml up --build

logs:
	docker compose logs -f

down:
	docker compose down

migrate:
	docker compose exec provet alembic upgrade head
