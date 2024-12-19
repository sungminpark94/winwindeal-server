#!/bin/sh
set -e
python3 manage.py migrate # 실행 전에 migrate 자동실행
python3 manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 winwindeal_be.wsgi:application --workers 2