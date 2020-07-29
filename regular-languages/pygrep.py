#!/usr/bin/env python2
"""
pygrep.py
"""
from __future__ import print_function

import re, sys

pat = re.compile(sys.argv[1])

for line in sys.stdin:
  m = pat.match(line)
  if m:
    print(m.groups())
