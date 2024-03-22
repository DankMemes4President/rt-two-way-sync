#!/bin/bash

echo "Waiting for database to be ready..."

while ! nc -z "rtws-postgres" "5432"; do
  sleep 1
done

echo "Database is ready!"

python postgres-to-kafka.py
exec "$@"