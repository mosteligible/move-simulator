build-routing-engine:
	cd docker-routing-engine && ./build.sh

docker-compose:
	docker compose up --build -d

pre-commit:
	pre-commit run --all-files

build-simulator:
	docker build -t simulator:latest -f ./backend/Dockerfile ./backend
