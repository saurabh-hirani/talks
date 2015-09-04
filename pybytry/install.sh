#!/bin/bash

# ideally should be done via pip, setup.py

[[ $UID != 0 ]] && echo 'ERROR: run as root' && exit 1

pip install requests
pip install grequests
pip install flask

mkdir -p /var/tmp/pybytry
cd /var/tmp/pybytry

git clone https://github.com/saurabh-hirani/jsonchecker
git clone https://github.com/saurabh-hirani/jsonserver
git clone https://github.com/saurabh-hirani/pyfunc
