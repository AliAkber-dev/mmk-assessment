#!/bin/bash
cd /home/ubuntu/mmk-app
source app-env/bin/activate
export FLASK_APP=server/app.py
export FLASK_ENV=production