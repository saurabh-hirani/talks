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

cli="$parser_type/cli.py"

set -x

python $cli 
python $cli get 
python $cli get ip
python $cli get user-agent 
python $cli get headers
python $cli get html
python $cli get ip --show-env
python $cli get status 404

python $cli post payload
python $cli post -u username -p password payload
python $cli post -t token payload
python $cli post payload

python $cli put -u username -p password payload
python $cli put -t token payload

python $cli delete -u username -p password -t token payload
python $cli delete -t token payload

set +x
