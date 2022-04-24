#!/bin/bash
pip install virtualenv
cd /home/ubuntu/mmk-app
python -m pip install --upgrade pip
virtualenv app-env
pip install -r requirements.txt
apt-get install -y redis-tools redis-server
