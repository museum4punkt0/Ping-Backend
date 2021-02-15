#!/bin/bash
./manage.py collectstatic --noinput
uwsgi --ini ${APP_PATH}/deploy/docker/python/uwsgi.ini
