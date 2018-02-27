#!/usr/bin/env python
'''
Usage:
    httpbin [--verbose] get (ip|user-agent|headers|html) [--show-env]
    httpbin [--verbose] get status <status_code>
    httpbin [--verbose] post [(--username=<username> --password=<password>|--api-token=<api_token>)] <json_data>
    httpbin [--verbose] put [(--username=<username> --password=<password>|--api-token=<api_token>)] <json_data>
    httpbin [--verbose] delete (--username=<username> --password=<password>|--api-token=<api_token>)
    httpbin -h | --help
    httpbin --version

Options:
    -h|--help                  show this help text.
    <status_code>              status code to return.
    <json_data>                json_data to pass.
    -v, --verbose              verbose
    -V, --version              print this version.
    -u,--username <username>   request username. [default: admin]
    -p,--password <password>   request password. [default: admin]
    -t,--api-token <api_token> api token. [default: token]
'''

from __future__ import print_function
import sys
from docopt import docopt
import json
from schema import Schema, And, Use, Optional

def call_url(args):
  ''' Call the target url '''
  return True

def validate_input(args):
  ''' Validate input '''
  # check https://github.com/saurabh-hirani/talks/blob/master/docopt/rule_filter.py
  validation_schema = Schema({
    'status_code': And(Use(int), lambda n: 100 <= n <= 599),
    'username': And(str, Use(str.lower), lambda s: s in ('user1', 'user2')),
    'password': And(str, len),
    'api_token': And(str, len)
  })
  validation_schema.validate(args)

def load_args(args):
  ''' Load command line args '''
  parsed_docopt = docopt(__doc__, version='1.0')
  return parsed_docopt

if __name__ == '__main__':
  args = load_args(sys.argv[1:])
  validate_input(args)
  print(json.dumps(args, indent=2))
  call_url(args)
