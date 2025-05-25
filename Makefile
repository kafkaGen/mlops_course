run-services:
	docker compose --env-file .env -f docker/docker-compose.yaml -p mlops_course up -d

stop-services:
	docker compose -p mlops_course down
	