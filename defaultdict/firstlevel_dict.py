#!/usr/bin/env python

from collections import defaultdict

firstlevel_dict = defaultdict(dict)

print firstlevel_dict['a']

try:
  firstlevel_dict['a']['b']
except KeyError as e:
  print 'firstlevel_dict - Keyerror: %s' % e
