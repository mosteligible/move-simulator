build-routing-engine:
	cd docker-routing-engine && ./build.sh

docker-compose: build-routing-engine
	docker compose up --build -d

pre-commit:
	pre-commit run --all-files
