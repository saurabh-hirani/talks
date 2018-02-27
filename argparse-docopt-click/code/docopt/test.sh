#!/bin/bash -x

python cli.py 
python cli.py get 
python cli.py get ip
python cli.py get user-agent 
python cli.py get headers
python cli.py get html
python cli.py get ip --show-env
python cli.py get status 404
python cli.py post -u username -p password payload
python cli.py post -t token payload
python cli.py post payload
python cli.py delete payload
python cli.py delete -t token payload
