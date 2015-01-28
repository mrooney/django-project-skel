#!/bin/bash
set -e
python manage.py migrate --noinput
python manage.py test {{ project_name }} 2>&1
