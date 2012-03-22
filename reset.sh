#!/bin/bash
dropdb helios
createdb helios
python manage.py syncdb
python manage.py migrate
