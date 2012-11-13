#!/bin/bash
set -e
python manage.py syncdb --migrate --noinput | egrep -v "(Installed 0|Nothing to migrate|Loading initial data)"
python manage.py test {{ project_name }} 2>&1
