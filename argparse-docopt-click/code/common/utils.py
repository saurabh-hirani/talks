''' Common utils '''

import argparse
from schema import Schema, And, Use, Optional, SchemaError
import uuid
import json


def get_username_schema():
  ''' username schema '''
  return Schema(And(str, lambda s: len(s) > 3 and s.startswith('user')),
                error='Invalid username')

def validate_username_arg(username):
  ''' validate username input '''
  try:
    get_username_schema().validate(username)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return username

def get_password_schema():
  ''' password schema '''
  return Schema(And(str, lambda s: len(s) > 6 and s in ['password1',
                                                        'password2']),
                error='Invalid password')

def validate_password_arg(password):
  ''' validate password input '''
  try:
    get_password_schema().validate(password)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return password

def get_json_schema():
  ''' json schema '''
  return Schema(Use(json.loads), error='Invalid json')

def validate_json_arg(json_data):
  ''' validate json input '''
  try:
    get_json_schema().validate(json_data)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return json_data

def get_uuid_schema():
  ''' uuid schema '''
  return Schema(Use(uuid.UUID), error='Invalid uuid')

def validate_uuid_arg(uuid_data):
  ''' validate uuid input '''
  try:
    get_uuid_schema().validate(uuid_data)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return uuid_data

def get_status_code_schema():
  ''' http status code schema '''
  return Schema(And(Use(int),
                lambda n: 100 <= n <= 599,
                error='Invalid status_code - should be between 100 and 599'))

def validate_status_code_arg(status_code):
  ''' validate status_code input '''
  try:
    get_status_code_schema().validate(status_code)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return status_code
