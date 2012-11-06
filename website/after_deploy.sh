#!/bin/bash
set -e
python manage.py syncdb --migrate
python manage.py test {{ project_name }} 2>&1
