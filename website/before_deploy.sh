#!/bin/bash
set -ex
pip install -r ../requirements.txt | grep -v "(Requirement already satisfied|Cleaning up)"
python manage.py collectstatic --noinput
