#!/usr/bin/env python

''' Click example '''

from __future__ import print_function
import common.utils as utils
import os
import sys
import click

@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, **kwargs):
  ''' top level cli '''
  this_function_name = sys._getframe().f_code.co_name
  click.echo('function %s: verbosity=%s' % (this_function_name, kwargs['verbose']))
  ctx.obj['log_level'] = 'info'

@cli.command()
@click.argument('get_type')
@click.option('--status-code', '-s', default=404, help='return status code',
              callback=utils.click_validate_status_code_arg)
@click.option('--show-env', default=False, is_flag=True, help='show env vars')
@click.pass_context
def get(ctx, **kwargs):
  ''' Get method call '''
  this_function_name = sys._getframe().f_code.co_name
  print('function %s: ctx.obj.log_level=%s' % (this_function_name, ctx.obj['log_level']))
  print("SUCCESS\n")

@cli.command()
@click.argument('json_data', callback=utils.click_validate_json_arg)
@click.option('--username', '-u', help='username',
              callback=utils.click_validate_username_arg,
              default=lambda: os.environ.get('CLI_USERNAME', 'envvar'))
@click.option('--password', '-p', help='password',
              callback=utils.click_validate_password_arg,
              default=lambda: os.environ.get('CLI_PASSWORD', 'envvar'))
@click.option('--api-token', '-t', callback=utils.click_validate_uuid_arg, 
              help='api-token', default='2a9d52eb-1c66-11e8-9997-a0999b0f9f4b')
@click.pass_context
def post(ctx, **kwargs):
  ''' Post method call '''
  this_function_name = sys._getframe().f_code.co_name
  print('function %s: ctx.obj.log_level=%s' % (this_function_name, ctx.obj['log_level']))
  print("SUCCESS\n")

@cli.command()
@click.argument('json_data', callback=utils.click_validate_json_arg)
@click.option('--username', '-u', help='username',
              callback=utils.click_validate_username_arg,
              default=lambda: os.environ.get('CLI_USERNAME', 'envvar'))
@click.option('--password', '-p', help='password',
              callback=utils.click_validate_password_arg,
              default=lambda: os.environ.get('CLI_PASSWORD', 'envvar'))
@click.option('--api-token', '-t', callback=utils.click_validate_uuid_arg,
              help='api-token', default='2a9d52eb-1c66-11e8-9997-a0999b0f9f4b')
@click.pass_context
def put(ctx, **kwargs):
  ''' Put method call '''
  this_function_name = sys._getframe().f_code.co_name
  print('function %s: ctx.obj.log_level=%s' % (this_function_name, ctx.obj['log_level']))
  print("SUCCESS\n")

@cli.command()
@click.option('--username', '-u', help='username', 
              callback=utils.click_validate_username_arg,
              default=lambda: os.environ.get('CLI_USERNAME', 'envvar'))
@click.option('--password', '-p', help='password',
              callback=utils.click_validate_password_arg,
              default=lambda: os.environ.get('CLI_PASSWORD', 'envvar'))
@click.option('--api-token', '-t', callback=utils.click_validate_uuid_arg,
              help='api-token', default='2a9d52eb-1c66-11e8-9997-a0999b0f9f4b')
@click.pass_context
def delete(ctx, **kwargs):
  ''' Delete method call '''
  this_function_name = sys._getframe().f_code.co_name
  print('function %s: ctx.obj.log_level=%s' % (this_function_name, ctx.obj['log_level']))
  print("SUCCESS\n")

@cli.group()
@click.option('--username', '-u', help='username', 
              callback=utils.click_validate_username_arg,
              default=lambda: os.environ.get('CLI_USERNAME', 'envvar'))
@click.option('--password', '-p', help='password',
              callback=utils.click_validate_password_arg,
              default=lambda: os.environ.get('CLI_PASSWORD', 'envvar'))
@click.option('--api-token', '-t', callback=utils.click_validate_uuid_arg, 
              help='api-token', default='2a9d52eb-1c66-11e8-9997-a0999b0f9f4b')
@click.pass_context
def modify(ctx, **kwargs):
  ''' report data '''
  ctx.obj['cmd'] = 'report'
  ctx.obj['username'] = kwargs['username']
  ctx.obj['password'] = kwargs['password']
  ctx.obj['api-token'] = kwargs['api_token']

@modify.command()
@click.argument('json_data', callback=utils.click_validate_json_arg)
@click.pass_context
def post(ctx, **kwargs):
  ''' requests report '''
  this_function_name = sys._getframe().f_code.co_name
  print('function %s: ctx.obj.username=%s' % (this_function_name, ctx.obj['username']))
  print("SUCCESS\n")

@modify.command()
@click.argument('json_data', callback=utils.click_validate_json_arg)
@click.pass_context
def put(ctx, **kwargs):
  ''' requests report '''
  this_function_name = sys._getframe().f_code.co_name
  print('function %s: ctx.obj.username=%s' % (this_function_name, ctx.obj['username']))
  print("SUCCESS\n")

@modify.command()
@click.pass_context
def delete(ctx, **kwargs):
  ''' requests report '''
  this_function_name = sys._getframe().f_code.co_name
  print('function %s: ctx.obj.username=%s' % (this_function_name, ctx.obj['username']))
  print("SUCCESS\n")

if __name__ == "__main__":
  print("============================")
  cli(obj={})
  print("============================")
