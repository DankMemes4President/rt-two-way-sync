#!/bin/bash

echo "Waiting for database to be ready..."

while ! nc -z "rtws-postgres" "5432"; do
  sleep 1
done

echo "Database is ready!"

uvicorn webhook:app --host 0.0.0.0 --port 8080 --reload
exec "$@"