#!/usr/bin/python
"""
argv_to_sh.py

Embed an argv vector into a shell string, e.g. for ssh or sudo.
"""

import commands
import sys

s = ''
for arg in sys.argv[1:]:
  # strategy: double quote if it has ' --  otherwise single quote
  a = commands.mkarg(arg)
  sys.stdout.write(a)
