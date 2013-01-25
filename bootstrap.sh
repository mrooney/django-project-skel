#!/bin/bash
set -ex
git init .
git add .
git commit -am "initial commit"
virtualenv env
source env/bin/activate
pip install -r requirements.txt
mv manage.py website
chmod +x website/manage.py
cd website
./manage.py schemamigration {{projectname}} --initial