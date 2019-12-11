#!/bin/sh
apt-get install -y python3-pip
pip3 install -r requirements.txt
pyinstaller /code/start.py --onefile
