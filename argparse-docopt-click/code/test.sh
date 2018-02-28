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

valid_user="user1"
valid_password="password1"
valid_uuid="78f15402-1bb7-11e8-9aba-a0999b0f9f4b"
valid_payload="{\"a\": \"b\"}"
valid_status_code=404

set -x

# error
python $cli 

# error
python $cli get 

python $cli -v get ip
python $cli -v get user-agent 
python $cli -v get headers
python $cli -v get html
python $cli -v get ip --show-env

# error
python $cli -v get status 22

python $cli -v get status $valid_status_code

# error
python $cli -v post garbage_payload

# error
python $cli -v post -u garbage_username -p garbage_password garbage_payload

python $cli -v post -u $valid_user -p $valid_password "$valid_payload"

CLI_USERNAME=$valid_user CLI_PASSWORD=$valid_password python $cli -v post -u envvar -p envvar "$valid_payload"
CLI_USERNAME=$valid_user CLI_PASSWORD=$valid_password python $cli -v post "$valid_payload"

python $cli -v post -t $valid_uuid "$valid_payload"
python $cli -v post "$valid_payload"

# error
python $cli -v post -t garbage_token garbage_payload

python $cli -v post -t $valid_uuid "$valid_payload"

# error
python $cli -v put -u garbage_username -p garbage_password garbage_payload 

python $cli -v put -u $valid_user -p $valid_password "$valid_payload"
python $cli -v put -t $valid_uuid "$valid_payload"

# error
python $cli -v put "$valid_payload"

# error
python $cli -v delete

# error
python $cli -v delete -u garbage_username -p garbage_password -t token payload

python $cli -v delete -u $valid_user -p $valid_password
python $cli -v delete -t $valid_uuid 

# error
python $cli -v delete -t token

set +x
