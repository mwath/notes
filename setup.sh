#!/bin/sh

docker-compose exec --user=$UID --workdir=/app/api api alembic upgrade head
docker-compose exec db psql postgres postgres -c "INSERT INTO users(id, username, email, password) VALUES(0, 'DeletedAccount', 'deleted@deleted.de', '')"
