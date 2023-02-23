migrateup:
	alembic upgrade head

migratedown:
	alembic downgrade -1

composeup:
	docker compose up

test:
	docker compose run api sh -c "./test.sh"

protogen:
	python3 -m grpc_tools.protoc -I ./app/protos --python_out=./app/api/rpc/pb2 --grpc_python_out=./app/api/rpc/pb2 ./app/protos/*

.PHONY: migrateup migratedown composeup test protogen