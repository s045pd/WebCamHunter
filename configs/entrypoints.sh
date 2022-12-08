#!/bin/bash
python3 manage.py check
python3 manage.py createcachetable
python3 manage.py collectstatic --noinput
python3 manage.py migrate

export DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-admin}"
export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-admin}"
export DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@admin.com}"
python3 manage.py createsuperuser --noinput && echo -e "\033[0;32mcreated superuser[ $DJANGO_SUPERUSER_USERNAME:$DJANGO_SUPERUSER_PASSWORD ]\033[0m" || echo ''
python3 manage.py loaddata configs/data/*.json
python3 manage.py runscript init_data

# nginx
pm2 start configs/ecosystem.config.js
pm2 logs
