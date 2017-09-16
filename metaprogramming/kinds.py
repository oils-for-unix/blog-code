#!/usr/bin/python
"""
kinds.py
"""

import sys
import ast
import cStringIO

# Task:
# - Schema compiler?
# - Special case: Generate a named class with variable number of variables

NAMES = ['x', 'y', 'z', 'w']

def GenClassLexical(name, n):
  """After reader, before lexer."""
  f = cStringIO.StringIO()
  assert n <= len(NAMES), n

  # Note syntax errors:
  print >>f, 'class %s:' % name
  print >>f, '  def __init__(self):'

  for i in xrange(n):
    print >>f, '    self.%s = 0' % NAMES[i]

  return f.getvalue()


def GenClassParser(name, n):
  """After lexer, before parser."""
  # Use tokenize module?  Construct them manually?  But Python doesn't really
  # have access to its own tokenizer.
  pass


def GenClassAst(name, n):
  """After parser, before compiler."""
  print ast
  # compile()?
  pass


def GenClassBytecode(name, n):
  """After compiler, before runtime."""
  # BUILD_CLASS ?   Use opcode module?
  # compile()?
  pass


def GenClassReflection(name, n):
  # 
  cls = type(name, [], {})
  cls.__init__ = constructor




def main(argv):
  exec GenClassLexical('Point', 2)
  exec GenClassLexical('Quad', 4)
  print Point()
  print Quad()



if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print >>sys.stderr, 'FATAL: %s' % e
    sys.exit(1)
