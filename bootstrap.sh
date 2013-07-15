#!/bin/bash
set -ex
virtualenv env
source env/bin/activate
pip install -r requirements.txt
mv manage.py website
chmod +x website/manage.py
cd website
./manage.py schemamigration {{project_name}} --initial
chmod +x deploy.py before_deploy.sh after_deploy.sh
./deploy.py
cd ..
git init .
git add .
git add -f website/run/.gitignore
git commit -am "initial commit"
