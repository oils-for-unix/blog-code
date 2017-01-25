#!/usr/bin/python
"""
argv_to_sh.py

Embed an argv vector into a shell string, e.g. for ssh or sudo.
"""

import commands
import sys

# strategy: double quote if it has ' --  otherwise single quote
for arg in sys.argv[1:]:
  sys.stdout.write(commands.mkarg(arg))
