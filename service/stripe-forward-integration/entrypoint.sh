#!/bin/bash

echo "Waiting for database to be ready..."

while ! nc -z "rtws-postgres" "5432"; do
  sleep 1
done

echo "Database is ready!"

python __main__.py
exec "$@"