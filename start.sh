#!/bin/bash
set -e

echo "Running database migrations..."

poetry run alembic upgrade head

echo "Starting FastAPI application..."

exec poetry run uvicorn main:app --host 0.0.0.0 --port 8000
