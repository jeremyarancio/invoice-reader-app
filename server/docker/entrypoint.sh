#!/bin/bash
set -e

# Run database migrations
echo "Running database migrations..."
uv run alembic upgrade head

# Start the FastAPI server
echo "Starting FastAPI server..."
exec "$@"