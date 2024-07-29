#!/bin/sh

# define DJANGO SETTING as environment variable
export DJANGO_SETTINGS_MODULE="backend_server.settings"

# Wait for database launching

while ! pg_isready -h $SQL_HOST -p $SQL_PORT -U $SQL_USER > /dev/null 2>&1; do
	echo "Waiting for PostgreSQL to be ready..."
	sleep 1
done

# if [ ! -d "/app/backend_server" ]
# then 
# # Create Django project if not exist
#   echo "Create Django project Server... "
#   django-admin startproject backend_server
# fi
#
echo "Making migrations to transcendance_DB and collect static..."

# DB migration management

cd /app/backend_server
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

#launch server and listen Celery

python server_ignition.py

# daphne -b 0.0.0.0 -p 8001 backend_server.asgi:application
#
# # launch message broker
# echo "launching backend message broker"
# celery -A backend_server worker -l info

exec "$@"
