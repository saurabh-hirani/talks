#!/usr/bin/env python

from collections import defaultdict

thirdlevel_dict = defaultdict(dict)

thirdlevel_dict['a'] = defaultdict(dict)

thirdlevel_dict['a']['b'] = defaultdict(dict)

print thirdlevel_dict['a']['b']['c']

try:
  print thirdlevel_dict['a']['b']['c']['d']
except KeyError as e:
  print 'thirdlevel_dict - Keyerror: %s' % e
