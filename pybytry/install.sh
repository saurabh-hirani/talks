#!/bin/bash

# ideally should be done via pip, setup.py

[[ $UID != 0 ]] && echo 'ERROR: run as root' && exit 1

pip install requests
pip install grequests
