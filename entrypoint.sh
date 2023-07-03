#!/bin/sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export DEBIAN_FRONTEND=noninteractive
export SQL_ENGINE="django.db.backends.postgresql"
export SQL_DATABASE="django_rasa_prod"
export SQL_USER="postgres_rasa"
export SQL_PASSWORD="1234"
export SQL_HOST="165.227.170.110"
export SQL_PORT="5432"
export CHROMA_SERVER_HOST="165.227.170.110"
export N_RELATED_INTERACTIONS="5"

echo "Starting makemigrations"
python3 manage.py flush --no-input
python3 manage.py makemigrations
# python3 manage.py collectstatic --no-input
echo "Finished makemigrations"

echo "Starting migrate"
python3 manage.py migrate
echo "Finished migrate"

gunicorn app.wsgi:application --bind 0.0.0.0:5000 --timeout 0

exec "$@"