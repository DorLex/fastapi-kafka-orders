server:
	uvicorn src.app.main:app --reload

order_worker:
	python -m src.run_consumer

up:
	docker compose -f ./docker/docker-compose.yml up -d --build

infra:
	docker compose -f ./docker/docker-compose.yml --env-file ./.env up -d postgres # kafka kafka-ui

test:
	pytest -vv -s
