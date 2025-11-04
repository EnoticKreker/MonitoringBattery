#!/usr/bin/env sh
set -e

echo "Waiting for database at $DB_HOST:$DB_PORT..."
until nc -z $DB_HOST $DB_PORT; do
  echo "Database is not ready yet..."
  sleep 1
done
echo "Database is up!"

echo "Running Alembic migrations..."
export PYTHONPATH=/app/app:$PYTHONPATH
uv run alembic -c /app/app/alembic.ini upgrade head

echo "Seeding initial data..."
uv run /app/app/seed_data.py

echo "Starting server..."
cd /app/app
echo "Server starting in directory: $(pwd)"
echo "Server starting in directory: $(ls)"

exec uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload


