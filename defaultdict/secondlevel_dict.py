#!/usr/bin/env python

from collections import defaultdict

secondlevel_dict = defaultdict(dict)

secondlevel_dict['a'] = defaultdict(dict)

print secondlevel_dict['a']['b']

try:
  print secondlevel_dict['a']['b']['c']
except KeyError as e:
  print 'secondlevel_dict - Keyerror: %s' % e
