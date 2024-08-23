#!/bin/bash

# Start the Django server in the background
python manage.py runserver 0.0.0.0:8000 &

# Start the Celery worker in the background
celery -A djangoProject worker -l INFO &

# Start the Celery Beat scheduler in the background
celery -A djangoProject beat -l INFO &

# Wait for all background processes to complete
wait
