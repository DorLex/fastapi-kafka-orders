server:
	uvicorn src.app.main:app --reload

order_worker:
	python -m src.order_worker.main

up:
	docker compose -f ./docker/docker-compose.yml up -d --build

infra:
	docker compose -f ./docker/docker-compose.yml --env-file ./.env up -d postgres kafka-ui # kafka

test:
	pytest -vv -s
