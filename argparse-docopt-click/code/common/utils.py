''' Common utils '''

import argparse
import click
from schema import Schema, And, Use, Optional, SchemaError
import uuid
import json

def get_username_schema():
  ''' username schema '''
  return Schema(And(str, lambda s: len(s) > 3 and (s.startswith('user') or s == 'envvar')),
                error='Invalid username')

def argparse_validate_username_arg(username):
  ''' validate username input '''
  try:
    get_username_schema().validate(username)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return username

def click_validate_username_arg(ctx, param, value):
  ''' validate username input '''
  try:
    get_username_schema().validate(str(value))
  except SchemaError as ex:
    raise click.UsageError(str(ex))
  return value

def get_password_schema():
  ''' password schema '''
  return Schema(And(str, lambda s: len(s) > 3 and s in ['password1',
                                                        'envvar',
                                                        'password2']),
                error='Invalid password')

def argparse_validate_password_arg(password):
  ''' validate password input '''
  try:
    get_password_schema().validate(password)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return password

def click_validate_password_arg(ctx, param, value):
  ''' validate password input '''
  try:
    get_password_schema().validate(str(value))
  except SchemaError as ex:
    raise click.UsageError(str(ex))
  return value

def get_json_schema():
  ''' json schema '''
  return Schema(Use(json.loads), error='Invalid json')

def argparse_validate_json_arg(json_data):
  ''' validate json input '''
  try:
    get_json_schema().validate(json_data)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return json_data

def click_validate_json_arg(ctx, param, value):
  ''' validate json input '''
  try:
    get_json_schema().validate(str(value))
  except SchemaError as ex:
    raise click.UsageError(str(ex))
  return value

def get_uuid_schema():
  ''' uuid schema '''
  return Schema(Use(uuid.UUID), error='Invalid uuid')

def argparse_validate_uuid_arg(uuid_data):
  ''' validate uuid input '''
  try:
    get_uuid_schema().validate(uuid_data)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return uuid_data

def click_validate_uuid_arg(ctx, param, value):
  ''' validate uuid input '''
  try:
    get_uuid_schema().validate(str(value))
  except SchemaError as ex:
    raise click.UsageError(str(ex))
  return value

def get_status_code_schema():
  ''' http status code schema '''
  return Schema(And(Use(int),
                lambda n: 100 <= n <= 599,
                error='Invalid status_code - should be between 100 and 599'))

def argparse_validate_status_code_arg(status_code):
  ''' validate status_code input '''
  try:
    get_status_code_schema().validate(status_code)
  except SchemaError as ex:
    raise argparse.ArgumentTypeError(str(ex))
  return status_code

def click_validate_status_code_arg(ctx, param, value):
  ''' validate status_code input '''
  try:
    get_status_code_schema().validate(value)
  except SchemaError as ex:
    raise click.UsageError(str(ex))
  return value
