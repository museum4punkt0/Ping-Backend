#!/bin/sh
python manage.py migrate
python manage.py collectstatic
gunicorn mein_objekt.wsgi:application --bind 0.0.0.0:8000 --log-level debug --error-logfile "-"
