#!/bin/sh


python manage.py makemigrations --settings=cspc_web.settings_dev
python manage.py migrate --no-input --settings=cspc_web.settings_dev


exec "$@"