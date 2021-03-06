#!/usr/bin/env python
''' Argparse example '''

from __future__ import print_function
import os
import sys
import argparse
import common.utils as utils

VERBOSE=False

def call_url(args):
  ''' Call the target url '''
  pass

def load_args(argv):
  ''' Load command line args '''
  parser = argparse.ArgumentParser()
  parser.add_argument('--verbose', '-v',  action='store_true', default=False,
                      help='verbosity')
  subparsers = parser.add_subparsers(help='commands')

  # get parser
  get_parser = subparsers.add_parser('get', help='get command')
  get_parser.add_argument('get_type', action='store', 
                          help='type of get command',
                          choices=['ip', 'user-agent', 'headers', 'html', 'status'])
  get_parser.add_argument('--status-code', help='status data payload', default=404,
                           type=utils.argparse_validate_status_code_arg)
  get_parser.add_argument('--show-env', '-e', action='store_true', default=False,
                           help='show env vars')

  # post parser
  post_parser = subparsers.add_parser('post', help='post command')
  post_parser.add_argument('--username', '-u', action='store', required=False,
                           default=os.environ.get('CLI_USERNAME', None),
                           help='username', type=utils.argparse_validate_username_arg)
  post_parser.add_argument('--password', '-p', required=False,
                           default=os.environ.get('CLI_PASSWORD', None),
                           help='password', type=utils.argparse_validate_password_arg)
  post_parser.add_argument('--api-token', '-t', required=False, help='api-token', 
                           type=utils.argparse_validate_uuid_arg)
  post_parser.add_argument('json_data', help='json payload',
                           type=utils.argparse_validate_json_arg)
  
  # put parser
  put_parser = subparsers.add_parser('put', help='put command')
  put_parser.add_argument('--username', '-u', required=False,
                          default=os.environ.get('CLI_USERNAME', None),
                          help='username', type=utils.argparse_validate_username_arg)
  put_parser.add_argument('--password', '-p', required=False,
                          default=os.environ.get('CLI_PASSWORD', None),
                          help='password', type=utils.argparse_validate_password_arg)
  put_parser.add_argument('--api-token', '-t', required=False,
                          help='api-token', type=utils.argparse_validate_uuid_arg)
  put_parser.add_argument('json_data', help='json payload',
                          type=utils.argparse_validate_json_arg)

  # delete parser
  delete_parser = subparsers.add_parser('delete', help='delete command')
  delete_parser.add_argument('--username', '-u', required=False,
                             default=os.environ.get('CLI_USERNAME', None),
                             help='username', type=utils.argparse_validate_username_arg)
  delete_parser.add_argument('--password', '-p', required=False,
                             default=os.environ.get('CLI_PASSWORD', None),
                             help='password', type=utils.argparse_validate_password_arg)
  delete_parser.add_argument('--api-token', '-t', required=False,
                             help='api-token', type=utils.argparse_validate_uuid_arg)

  args = vars(parser.parse_args(argv[1:]))

  global VERBOSE
  VERBOSE = args['verbose']

  if not('username' in args and 'password' in args and 'api_token' in args):
    return args

  username_provided = args['username'] is not None
  password_provided = args['password'] is not None
  token_provided = args['api_token'] is not None

  if not ((username_provided and password_provided) or token_provided):

    if not token_provided:

      if not username_provided and not password_provided:
        print('ERROR: Provide at least one of username password or API token')
        sys.exit(1)

      username_and_password_provided = username_provided and password_provided
      if not username_and_password_provided:
        print('ERROR: Provide username password together - not either')
        sys.exit(1)

  return args

def main(args):
  ''' Main function '''
  print("----------------------------")
  args = load_args(args)
  print("SUCCESS\n")
  call_url(args)

if __name__ == '__main__':
  sys.exit(main(sys.argv))
