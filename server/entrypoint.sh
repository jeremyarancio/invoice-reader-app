#!/bin/sh
set -e

# Wait for PostgreSQL to be ready
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for database..."
  sleep 1
done

# Run Alembic migrations
alembic upgrade head

# Start the API
exec "$@"
