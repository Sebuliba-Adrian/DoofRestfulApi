#!/bin/bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

exec gunicorn -b 0.0.0.0:5001 run:app