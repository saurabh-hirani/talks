#!/usr/bin/env python
'''
Usage:
    httpbin [--verbose] get (ip|user-agent|headers|html) [--show-env]
    httpbin [--verbose] get status <status_code>
    httpbin [--verbose] post (--username=<username> --password=<password>|--api-token=<api_token>) <json_data>
    httpbin [--verbose] put (--username=<username> --password=<password>|--api-token=<api_token>) <json_data>
    httpbin [--verbose] delete (--username=<username> --password=<password>|--api-token=<api_token>)
    httpbin -h | --help
    httpbin --version

Options:
    -h|--help                  show this help text.
    <status_code>              status code to return.
    <json_data>                json_data to pass.
    -v,--verbose               verbose
    -V,--version               print this version.
    -u,--username <username>   username.
    -p,--password <password>   password.
    -t,--api-token <api_token> api token.
'''

from __future__ import print_function
import sys
from docopt import docopt
from schema import SchemaError
import json
import common.utils as utils
import uuid

VERBOSE=False

def call_url(args):
  ''' Call the target url '''
  print("SUCCESS\n")
  return True

def validate_input(args):
  ''' Validate input '''
  validators = {
    "--username":    utils.get_username_schema(),
    "<json_data>":   utils.get_json_schema(),
    "<status_code>": utils.get_status_code_schema(),
    "--password":    utils.get_password_schema(),
    "--api-token":   utils.get_uuid_schema()
  }

  errors = {}

  for key, validator in validators.iteritems():
    if args[key] is not None:
      try:
        validator.validate(args[key])
      except SchemaError as ex:
        errors[key] = {
          'value': args[key],
          'error': str(ex)
        }

  if errors:
    print('ERROR: Failed to validate input')
    print(json.dumps(errors, indent=2))
    sys.exit(1)

  global VERBOSE
  VERBOSE = args['--verbose']

  return True

def load_args(args):
  ''' Load command line args '''
  parsed_docopt = docopt(__doc__, version='1.0')
  return parsed_docopt

if __name__ == '__main__':
  print("----------------------------")
  args = load_args(sys.argv[1:])
  print("++++++++++++++++++++++++++++\n")
  validate_input(args)
  call_url(args)
