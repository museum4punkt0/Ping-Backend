#!/bin/bash
./manage.py collectstatic
uwsgi --ini ${APP_PATH}/deploy/docker/python/uwsgi.ini
