#!/bin/bash
set -ex
pip install -qr ../requirements.txt
python manage.py collectstatic --noinput
