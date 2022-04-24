#!/bin/bash
cd /home/home/mmk-app
source app-env/bin/activate
export FLASK_APP=server/app.py
export FLASK_ENV=production
gunicorn --bind 127.0.0.1:5000  wsgi:app