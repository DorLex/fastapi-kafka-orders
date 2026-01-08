server:
	uvicorn src.app.main:app --reload

order_worker:
	python -m src.order_worker.main

up:
	docker compose -f ./docker/docker-compose.yml --env-file ./docker/.env up -d --build

infra:
	docker compose -f ./docker/docker-compose.yml --env-file ./docker/.env up -d postgres kafka kafka-ui

test:
	pytest -vv -s
