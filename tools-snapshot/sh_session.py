#!/usr/bin/python
"""
sh_session.py

Used with snip.py to generate a shell session.
"""

import sys


# Remove this stuff because we're adding our own
PREFIX = '<div class="highlight"><pre>'
SUFFIX = '</pre></div>'


def MultiLineSession(argv):
  with open(argv[1]) as f:
    html = f.read().strip()
  with open(argv[2]) as f:
    output = f.read()

  if html.startswith(PREFIX):
    html = html[len(PREFIX) : ]
  if html.endswith(SUFFIX):
    html = html[ : -len(SUFFIX)]

  out = sys.stdout.write

  out('<pre>')

  out('<span class="highlight">')
  for i, line in enumerate(html.splitlines(True)):
    if i == 0:
      out('$ ')
    else:
      out('&gt; ')  # > PS2 continuation
    out(line)

  out('</span>')

  if output:
    out('<span class="stdout">')
    out(output.rstrip())
    out('</span>\n')
  else:
    out('<span style="font-style: italic">... no output ...</span>\n')
  out('</pre>')


def main(argv):
  MultiLineSession(argv)

  # TODO:
  # LineByLineSession()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print >>sys.stderr, 'FATAL: %s' % e
    sys.exit(1)
