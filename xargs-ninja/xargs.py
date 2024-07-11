#!/usr/bin/env python3
"""
xargs.py

- asyncio
  - streams / readline
  - queues
  - semaphores?
- multiprocessing.Pool - not sure if this is a good API

We're using Python 3 because it supports descriptor passing.
"""
from __future__ import print_function

import asyncio
import optparse
import os
import sys
import subprocess


def log(msg, *args):
    if args:
        msg = msg % args
    print(msg, file=sys.stderr)


def main(argv):
    p = optparse.OptionParser(__doc__)
    p.add_option(
      '-I', dest='this', default='{}',
      help='this variable')
    p.add_option(
      '-P', dest='max_procs', default=1, type='int',
      help='maximum number of parallel processes')
    p.add_option(
      '--asyncio', dest='asyncio', action='store_true',
      help='use asyncio')

    opts, argv = p.parse_args(argv[1:])

    items = sys.stdin.readlines()
    print(items)

    if opts.asyncio:
        for item in items:
            child_argv = [a.replace('{}', item) for a in argv]
            log('%s', child_argv)
            status = subprocess.call(child_argv)
            log('%s', status)

        # TODO: on stdout
        # - asyncio readline
        # - figure out how to read netstring
        #   - asyncio can do it directly
        #   - in a mycpp/C++ event loop, do we use Ragel / re2c --storable state?
    else:
        # How would I implement -P here?

        # queue.Queue()?
        # We have to start it asynchronously
        # Popen() object
        # p.start()
        #
        # and then enter an event loop that does NOT do p.poll()
        #
        # it does waitpid() or something?
        # 
        # Do we use a lower level API?
        #
        # os.waitpid(-1) I guess
        # That gets the next failure
        #
        # The problem is we want to wait on:
        #
        # - process death
        # - queue slot
        #
        # At the SAME TIME
        #
        # Do we use the self-pipe trick?

        for item in items:
            child_argv = [a.replace('{}', item) for a in argv]
            log('%s', child_argv)
            status = subprocess.call(child_argv)
            log('%s', status)

    print(argv)
    return




if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
