#!/bin/sh

# define DJANGO SETTING as environment variable
export DJANGO_SETTINGS_MODULE="backend_server.settings"

# Wait for database launching 

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ ! -d "/app/backend_server" ]
then 
# Create Django project if not exist
  echo "Create Django project Server... "
  django-admin startproject backend_server
fi

echo "Make migrations and collect static..."

# DB migration management

cd /app/backend_server
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

#launch server
daphne -b 0.0.0.0 -p 8001 backend_server.asgi:application

# launch message broker
echo "launching backend message broker"
celery -A backend_server worker -l info

exec "$@"
