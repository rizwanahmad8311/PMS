#!/bin/bash

# Load environment variables from .env file
cp .env.docker .env

if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Install requirements
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Reset db data
python manage.py flush --noinput

# Create superuser with email and password
python manage.py createsuperuser --noinput

# Configure permissions in module permission
python manage.py configure_permissions

# Runserver
python manage.py runserver 0.0.0.0:8000
