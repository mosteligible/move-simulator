docker-compose:
	docker compose up --build

pre-commit:
	pre-commit run --all-files
