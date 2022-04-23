#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
apt-get install -y redis-tools redis-server
