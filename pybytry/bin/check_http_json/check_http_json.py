#!/usr/bin/env python

# TODO
# match non number warning and crit values
# have a function for each type of each - match_key, match_key against limits, etc.
# match multiple keys with key:value:warn:crit
# use ordered dict for output

import os
import sys
import argparse
import json
import imp

import utils

CHECK_URL_TIMEOUT = 60

def check_json(kwargs):
  urls = ['http://%s:%d%s' % (kwargs['host'], kwargs['port'], kwargs['uri'])]

  # if port range speciefied create multiple urls
  if kwargs['nports']:
    for port in range(kwargs['port'], kwargs['port'] + kwargs['nports']):
      urls.append('http://%s:%d%s' % (kwargs['host'], int(port), kwargs['uri']))

  # flag to check if one / many urls
  many_urls = True
  if len(urls) == 1:
    many_urls = False

  kwargs['timeout'] = CHECK_URL_TIMEOUT

  # make parallel http get requests
  responses = utils.do_parallel_http_get(urls, kwargs)

  valid_responses = {}
  invalid_responses = {}

  for url, response in responses.iteritems():
    if response.status_code == 200:
      valid_responses[url] = response
      continue

    invalid_responses[url] = response

  # validate if urls returned 200
  #valid_responses = responses.keys()
  #invalid_responses = set(urls) - set(valid_responses)

  valid_urls = {}
  invalid_urls = {}

  for url, response in valid_responses.iteritems():
    valid_urls[url] = response.json()
    if kwargs['verbose']:
      print "------url------"
      print 'url: %s' % url
      print 'valid'
      print json.dumps(valid_urls[url], indent=4)
      print "\n"

  if invalid_responses:
    for url, response in invalid_responses.iteritems():
      invalid_urls[url] = response.json()
      if kwargs['verbose']:
        print "------url------"
        print 'url: %s' % url
        print json.dumps(invalid_urls[url], indent=4)
        print "\n"

    print 'CRITICAL: Problem detected. See detailed output'
    print json.dumps({
      'invalid_urls': invalid_urls,
      'valid_urls': valid_urls,
    }, indent=4)
    return 2

  chk_entities = ['match_key', 'match_key_val', 'callback_path', 'callback_module']
  chk_something = any([x is not None for x in chk_entities if kwargs[x]])
  if not chk_something:
    print 'OK: just checked if urls are reachable'
    print json.dumps(valid_urls, indent=4)
    return 0

  # perform checks on valid urls

  # now we will get a new set of valid urls depending on check - save the oldies
  old_valid_urls = {}
  old_valid_urls.update(valid_urls)

  invalid_urls = {}
  valid_urls = {}
  for url, json_ds in old_valid_urls.iteritems():

    # do match key checks
    if kwargs['match_key']:
      match_key = kwargs['match_key']

      if match_key not in json_ds:
        invalid_urls[url] = 'Did not match %s' % match_key
        continue

      if url not in valid_urls:
        valid_urls[url] = []

      valid_urls[url].append('Matched key %s' % match_key)

    match_val = None

    # do match key val checks
    if kwargs['match_key_val']:
      match_key, match_val = kwargs['match_key_val'].split(kwargs['key_sep'])

      if match_key not in json_ds:
        invalid_urls[url] = 'Did not match %s' % match_key
        continue

      if str(json_ds[match_key]) != str(match_val):
        invalid_urls[url] = 'Key %s != %s' % (match_key, match_val)
        continue

      if url not in valid_urls:
        valid_urls[url] = []

      valid_urls[url].append('Matched keyval %s = %s' % (match_key, match_val))

    # no values to check against match key value
    if 'warning' not in kwargs:
      continue

    # check thresholds
    if kwargs['match_key'] or kwargs['match_key_val']:
      if not match_val:
        match_val = json_ds[match_key]

      if kwargs['are_limits_nos']:
        state = 'ok'
        if float(match_val) >= float(kwargs['warning']):
          state = 'warning'
        if float(match_val) >= float(kwargs['critical']):
          state = 'critical'

        if state != 'ok':
          invalid_urls[url] = {
            'match_key': match_key,
            'match_key_value': float(match_val),
            'crossed_limit': state,
            'crossed_limit_value': float(kwargs[state])
          }
          del valid_urls[url]
          continue

        if url not in valid_urls:
          valid_urls[url] = []

        valid_urls[url].append({
          'match_key': match_key,
          'match_key_value': float(match_val),
          'warning_value': float(kwargs['warning']),
          'critical_value': float(kwargs['critical']),
        })

    # do callback checks
    if kwargs['callback_path']:
      if not os.path.exists(kwargs['callback_path']):
        print 'CRITICAL: Callback path %s does not exist' % kwargs['callback_path']
        return 2

      mod = imp.load_source('callback', kwargs['callback_path'])
      try:
        output = getattr(mod, kwargs['callback_func'])(kwargs, json_ds)
      except AttributeError:
        print 'CRITICAL: %s does not have attr %s' % (mod, kwargs['callback_func'])
        return 2

      if output['state'] != 'OK':
        invalid_urls[url] = output['msgs']
      else:
        valid_urls[url] = output['msgs'] or 'OK: All good'

  if invalid_urls:
    print 'CRITICAL: Check detailed output.'
    print json.dumps({
      'invalid_urls': invalid_urls,
      'valid_urls': valid_urls,
    }, indent=4)
    return 2

  print 'OK: All good'
  print json.dumps(valid_urls, indent=4)
  return 0

def validate(args):
  invalid_invoc_msg = 'UNKNOWN: Invalid invocation - ' 

  if not args['uri'].startswith('/'):
    print invalid_invoc_msg + 'uri should start with single /'
    sys.exit(3)

  # check if mutually exclusive args are not specified
  # wanted to keep it simple - avoided using parser.add_mutally_exclusive_group
  if (args['warning'] is not None) ^ (args['critical'] is not None):
    print invalid_invoc_msg + 'either provide both warning and critical or none'
    sys.exit(3)

  if args['callback_path'] and args['callback_module']:
    print invalid_invoc_msg + 'cannot specify both callback_path and callback_module'
    sys.exit(3)

  if (args['callback_path'] or args['callback_module']) and not args['callback_func']:
    print invalid_invoc_msg + 'callback_func not specified'
    sys.exit(3)

  # check if limits are nos.
  is_warning_num = is_critical_num = args['are_limits_nos'] = True

  try:
    args['warning'] = float("%.2f" % float(args['warning']))
  except (TypeError, ValueError):
    args['are_limits_nos'] = False
    is_warning_num = False

  try:
    args['critical'] = float("%.2f" % float(args['critical']))
  except (TypeError, ValueError):
    is_critical_num = False

  if is_warning_num ^ is_critical_num is True:
    print invalid_invoc_msg + 'cannot have different data types for warning and critical'
    sys.exit(2)

  return True

def parse_cmdline(args):
  desc = 'Check http json response'
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument('-H', '--host', help='host to check', required=True)
  parser.add_argument('-p', '--port',
                      help='check port for the host - not comptabile with ' +\
                      'base_port or nports',
                      type=int,
                      required=True)
  parser.add_argument('--username', help='username for basic auth', 
                      type=str,
                      default=None)
  parser.add_argument('--password', help='password for basic auth', 
                      type=str,
                      default=None)
  parser.add_argument('--uri', help='uri to use', required=True)
  parser.add_argument('--nports',
                      help='check from port to port + nports',
                      type=int)
  parser.add_argument('--match_key',
                      help='check if this key is present',
                      type=str,
                      default=None)
  parser.add_argument('--match_key_val',
                      help='check if key:value is present where : is --key_sep',
                      type=str,
                      default=None
                     )
  parser.add_argument('--key_sep',
                      help='check if this key is present',
                      type=str,
                      default=':')
  parser.add_argument('--warning',
                      help='warn if key value matches this limit - ' +\
                      'needs match_key - does the right threshold matching for int/float',
                      type=str,
                      default=None)
  parser.add_argument('--critical',
                      help='critical if key value matches this limit - ' +\
                      'needs match_key - does the right threshold matching for int/float',
                      type=str,
                      default=None)
  parser.add_argument('--callback_path',
                      help='load callback module from this path and '+
                      'do what callback_module does - cannot specify both',
                      type=str,
                      default=None)
  parser.add_argument('--callback_module',
                      help='pass the json output to this callback_module.main - ' +\
                      'does AND with rest of the conditions',
                      type=str,
                      default=None)
  parser.add_argument('-v','--verbose', action='store_true', default=False)
  parser.add_argument('--callback_func',
                      help='pass the json output to this callback_module.callback_func -' +\
                           'does AND with rest of the conditions',
                      type=str,
                      default=None)

  try:
    args = vars(parser.parse_args())
  except SystemExit:
    # override system exit so that we can give icinga specific message
    # i.e. messages prefixed by either OK/WARN/CRITICAL/UNKNOWN and
    # control exit status - 0/1/2/3 for OK/WARN/CRITICAL/UNKNOWN
    # but skip this scenario if user asked for help message
    if '--help' in args or '-h' in args:
        sys.exit(0)
    err = 'UNKNOWN: Invalid invocation'
    print err
    sys.exit(3)

  if args['verbose']:
    print "------args------"
    print json.dumps(args, indent=4)

  return args

def main():
  args = parse_cmdline(sys.argv)
  validate(args)
  return check_json(args)

if __name__ == '__main__':
  sys.exit(main())
