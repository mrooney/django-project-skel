#!/bin/bash
set -ex
python manage.py migrate
python manage.py test contextcards
