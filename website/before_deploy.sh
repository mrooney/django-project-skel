#!/bin/bash
set -ex
python manage.py collectstatic --noinput
pip install -r ../requirements.txt
