#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"; do
  sleep 2
done

TABLE_EXISTS=$(PGPASSWORD="$DB_PASS" psql \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  -tAc "SELECT 1 FROM information_schema.tables WHERE table_name = 'users' LIMIT 1;")

if [ "$TABLE_EXISTS" != "1" ]; then
  echo "Applying SQL schema from src/tasks.sql..."
  PGPASSWORD="$DB_PASS" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -f src/tasks.sql
else
  echo "Database schema already exists, skipping src/tasks.sql"
fi

exec uvicorn main:app --app-dir src --host 0.0.0.0 --port 8000
