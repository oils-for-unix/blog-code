#!/usr/bin/python -S
"""Expand text snippets in a file.

Usage:
  snip [options] <file>...
  snip -h | --help
  snip --version

Options:
  --script=SCRIPT
      Execute this script.  By default, if you pass 'foo.txt', it looks for an
      executable named 'foo.snip' in the current directory, then a file called
      'Snip'.  'Snip' is generally used for all files in a directory.

Examples:

  $ ls
  Snip index.txt

  $ cat index.txt
  $ cat Snip

  $ snip index.txt
  ...

It's important not to rely on the order of execution of snippets.  That is, the
snippets functions should produce just stdout, not side effects.
"""
# TODO: Write a doctest-style example above?


import optparse
import os
import subprocess
import sys

ECHOING = 0
SNIPPING = 1

# TODO: Don't use raw subprocess.  Need to respect -v and so forth.

def ExpandSnippets(in_stream, script):
  """Print to stdout."""

  state = ECHOING
  captured = []
  snip_argv = None  # used for both ==> and -->

  for i, line in enumerate(in_stream):
    #print i, state

    # Insert snippets
    if line.startswith('==>'):
      # No quoting -- just raw split
      snip_argv = line[3:].strip().split()

      child_argv = [script] + snip_argv

      # Capture stdout.
      try:
        p = subprocess.Popen(child_argv, stdout=subprocess.PIPE)
      except OSError, e:
        # TODO: error handling below, and better handling in general
        print >>sys.stderr, 'Error running %s: %s' % (child_argv, e)
        raise

      for line in p.stdout:
        sys.stdout.write(line)

      # Don't process anything else.
      continue

    # Change states
    if line.startswith('-->'):
      # TODO: if state is already SNIPPING, then issue warning?
      state = SNIPPING
      snip_argv = line[3:].strip().split()
      if not snip_argv:
        # 1-based line number.
        # TODO: Better error handling
        raise RuntimeError('Line %d has no command: %r' % (i+1, line))

    # First act on the state
    if state == ECHOING:
      # echo a normal line
      sys.stdout.write(line)

    elif state == SNIPPING:
      captured.append(line)

    # This test happens AFTER the sys.stdout.write above, so we don't echo this
    # line.
    if line.startswith('<--'):
      # TODO: if state is already ECHOING, then issue warning?
      state = ECHOING

      # Now that we got the end marker, pipe it in to the script.
      #print captured  # TODO: log this

      if snip_argv == ['omit']:  # COMMENT
        captured = []  # RESET
        continue

      # TODO: Is "include" also a command?  That can be handled by the shell
      # easily though.

      child_argv = [script] + snip_argv
      stdin_str = ''.join(captured[1:-1])

      p = subprocess.Popen(child_argv, stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
      captured_stdout, _ = p.communicate(input=stdin_str)

      exit_code = p.wait()
      if exit_code != 0:
        raise RuntimeError('%s exited with code %d' % (child_argv, exit_code))

      sys.stdout.write(captured_stdout)

      captured = []  # RESET for next snippet


def main(argv):
  """Returns an exit code."""

  p = optparse.OptionParser(__doc__, version='snip 0.1')
  p.add_option(
      '--script', dest='script', default=None, type=str,
      help='The Snip script to execute')

  opts, argv = p.parse_args(argv[1:])

  for filename in argv:
    if filename == '-':
      in_stream = sys.stdin
    else:
      try:
        in_stream = open(filename)
      except IOError, e:
        raise RuntimeError(e)

    script = opts.script
    if not script:
      base, _ = os.path.splitext(filename)
      script1 = base + '.snip'

      script2 = os.path.join(os.path.dirname(filename), 'Snip')

      if os.path.exists(script1):
        script = script1
      elif os.path.exists(script2):
        script = script2
      else:
        raise RuntimeError('Neither %s or %s exists' % (script1, script2))

    ExpandSnippets(in_stream, script)

  return 0


if __name__ == '__main__':
  try:
    sys.exit(main(sys.argv))
  except RuntimeError, e:
    print >>sys.stderr, 'snip: %s' % e.args[0]
    sys.exit(1)
  except KeyboardInterrupt, e:
    print >>sys.stderr, 'snip: Interrupted.'
    sys.exit(1)
