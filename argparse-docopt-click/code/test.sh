#!/bin/bash

usage="$0 argparse|docopt|click"

if [[ $# -ne 1 ]]; then
  echo $usage
  exit 1
fi

parser_type=$1

if [[ $parser_type != 'argparse' ]] && [[ $parser_type != 'docopt' ]] && [[ $parser_type != 'click' ]]; then
  echo $usage
  exit 1
fi

cli="$parser_type-cli/cli.py"

set -x

python $cli 
python $cli get 
python $cli -v get ip
python $cli -v get user-agent 
python $cli -v get headers
python $cli -v get html
python $cli -v get ip --show-env
python $cli -v get status 404
python $cli -v get status 22

python $cli -v post payload
python $cli -v post -u username -p password payload
python $cli -v post -t token payload
python $cli -v post payload

python $cli -v put -u username -p password payload
python $cli -v put -t token payload

python $cli -v delete -u username -p password -t token payload
python $cli -v delete -t token payload

set +x
