#!/usr/bin/env python

from collections import defaultdict

def makehash():
  return defaultdict(makehash)

nlevel_dict = makehash()

print nlevel_dict['a']['b']['c']['d']['e']['f']['g']
nlevel_dict['a']['b']['c']['d']['e']['f']['g'] = [1,2,3]
print nlevel_dict
