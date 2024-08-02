#!/bin/bash

# Wait for database launching

while ! pg_isready -h $SQL_HOST -p $SQL_PORT -U $SQL_USER > /dev/null 2>&1; do
	echo "Waiting for PostgreSQL to be ready..."
	sleep 1
done

echo "PostgreSQL started"
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "Waiting for apps ..."
sleep 5


echo "ASGI server launching ..."
# python /app/manage.py runserver 0.0.0.0:8001
daphne -b 0.0.0.0 -p 8001 user_management.asgi:application

exec "$@"
