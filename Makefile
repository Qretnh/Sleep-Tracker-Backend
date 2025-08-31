.PHONY: migrate

migrate:
	docker-compose exec backend alembic -c /app/backend/alembic.ini upgrade head
