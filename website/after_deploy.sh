#!/bin/bash
set -ex
python manage.py syncdb --migrate
python manage.py test {{ project_name }}
