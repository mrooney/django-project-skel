#!/bin/bash
set -ex
pip install -r ../requirements.txt
python manage.py collectstatic --noinput
