repo-init:
	poetry install
	poetry shell
	pre-commit install

start-api-local:
	poetry run uvicorn app:app --reload --app-dir ./src

start-api-docker:
	docker run -p 8000:8000 api:latest

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

build-api:
	docker build -t api:latest -f ./build/docker/Dockerfile .
