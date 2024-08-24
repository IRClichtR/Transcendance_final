#!/bin/bash

export DJANGO_SETTINGS_MODULE=pythpong.settings

echo "Make migration for pong container ..."
cd pythpong
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "Waiting for apps ..."
sleep 5

echo "Launch ASGI server ..."
PYTHONUNBUFFERED=1 daphne -b 0.0.0.0 -p 8002 pythpong.asgi:application
# exec python -u manage.py runserver 0.0.0.0:8002

exec "$@"
