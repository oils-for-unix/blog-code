#!/usr/bin/env python3
from __future__ import print_function
"""
cat-brain - A language for Unix test workloads

- cat-brain: 
  - attached to a runtime that can implement simple Unix filters like 'cat',
  - dump argv env etc.

- sh-brain
  - can call system() on shell
  - can fork
  - can start threads, e.g. so you can inspect them
  - malloc - to use more memory - copy the whole tape

- null-brain
  - WASM

- bad-brain: does all sorts of bad things, is written in C
  - seg faults
    - dereference null
    - divide by zero
  - ubsan - integer behavior
  - asan - overflow
  - syscalls?
  - blowing the C call stack
    - how?
    - I think you just create a malicious stack


Language constructs:
  iteration: forever { } , repeat { }
  condition
  arbitrary computation: bf

  todo: are there subroutines?
    like def f x { }
    I think we can take one arg, which is either literal, or the register

Formats
  J8 strings only - what about JSON8 and TSV8?  It's a building block
  Netstrings

Protocols:
  FANOS with Unix domain sockets

Syscalls:
  time()
  getpid()
  exit()

  signal() - including kill USR1 etc.

  fork()
  create pthread

State:
  int counter, for iteration
  string register
  argv
  env

"""

import json
import os
import re
import time

# Syntax is a subset of POSIX shell.
# The program may only have spaces and newlines.
# There is no quoting - instead use commands like 'catbrain -c "space; tab;"'
# There is no ambiguity about whitespace.
#
#
# That's it 5 kinds of token
#
# - 5 tokens
# - 3 control flow
#   - repeat 3
#   - forever
#   - cond
# - 1 sublanguage: brainfuck
#
# - 3 registers
#   - s = working string
#   - argv
#   - env is a dict or what?
#     - I guess this is a KEY=value thing in C, so we should be powerful enough
#     to escape the value?
#     - we need a split operation
#
# - 2 concurrency constructs
#   - forking
#   - threading
#
# - all in ~1000 lines?
#
# Two kinds of sandboxing:
#   - secomp
#   - WASI - test if it works?
#
# wasm-brain - pure computation - . , is what?
# bad-brain
#   - it can dump raw structs from memory, like  
#
# Would also be nice to test if it boots QEMU

# BUILD
# - static linking
# - dynamic linking
#
# It's a script for testing I/O

# Testing:
# - BYO protocol
# 
# ./catbrain-test.sh case-foo

GRAMMAR = re.compile(r'''
    [ ]*                           # leading space OK
    ([a-z-]+)                      # command
    (?:
      [ ]+                         # at least one space
                                   # TODO: printable chars, including utf-8, but NOT space, newline
                                   # NOTE any shell chars
      ([a-zA-Z0-9_ /:=<>\[\].,+-]+)  # optional arg: \w chars and bf chars
    )?                             
    ([;\n]?)                       # terminator - if none terminator, we stop processing
''', re.VERBOSE)

# See catbrain.md
UNQUOTED = r'[a-zA-Z0-9_{}]+'
SQ = r"'[^']*'"
SEMI = r';'
NEWLINE = r'[\n]'
SPACE = r'[ ]'
COMMENT = SPACE + r'#[^\n]*'

# Comment must come before space
TOKENS = [UNQUOTED, SQ, SEMI, NEWLINE, COMMENT, SPACE]

LEXER_RE = re.compile('|'.join('(%s)' % pat for pat in TOKENS))


class Id:
    Word = 'w'
    Space = 's'
    Semi = ';'
    Newline = 'n'
    LBrace = '{'
    RBrace = '}'

    Eof = ''  # For parser


def Lex(code_str):
    tokens = []

    pos = 0
    n = len(code_str)

    while pos != n:
        m = LEXER_RE.match(code_str, pos)
        if not m:
            raise RuntimeError('Syntax error %r' % code_str[pos:pos+10])
        unquoted, sq, semi, newline, comment, space = m.groups()
        #print(m.groups())

        token = None
        if unquoted is not None:
            # Like YSH - this is the same as an unquoted word
            # We don't want it to be a separate token
            if unquoted == '{':
                token = (Id.LBrace, None)
            elif unquoted == '}':
                token = (Id.RBrace, None)
            else:
                if '{' in unquoted or '}' in unquoted:
                    raise RuntimeError("Word can't have unquoted { or }")
                token = (Id.Word, unquoted)
        elif sq is not None:
            token = (Id.Word, sq[1:-1])
        elif semi is not None:
            token = (Id.Semi, semi)
        elif newline is not None:
            token = (Id.Newline, newline)
        elif space is not None:
            pass  # skip spaces
        elif comment is not None:
            pass
        else:
            raise AssertionError()

        if token is not None:
            token_len = len(m.group(0))
            tok_id, tok_val = token
            tokens.append((tok_id, tok_val, pos, token_len))

        pos = m.end()

    tokens.append((Id.Eof, None, pos, 0))
    return tokens


class ParseError(RuntimeError):
    pass


class Parser(object):
    def __init__(self, code_str, tokens):
        self.code_str = code_str
        self.tokens = tokens
        # Must succeed since we have at least an Id.Eof token
        self.i = 0
        self.tok_id, self.tok_val, self.tok_pos, self.tok_len = self.tokens[self.i]

    def _Error(self, msg):
        # TODO: print the line and ^^^
        snippet = self.code_str[self.tok_pos:]
        return ParseError('Syntax error at pos %d: %s: %r' % (self.tok_pos, msg, snippet))

    def _Next(self):
        self.i += 1
        self.tok_id, self.tok_val, self.tok_pos, self.tok_len = self.tokens[self.i]
        #log('_Next %r %r', self.tok_id, self.tok_val)

    def _Eat(self, tok_id):
        if self.tok_id != tok_id:
            raise self._Error('Expected token %r, got %r' % (tok_id, self.tok_id))
        val = self.tok_val
        #log('tokens %s', self.tokens)
        #log('i %d', self.i)
        self._Next()
        return val

    def Program(self):
        """
        top = Eof
            | sequence Eof
        """
        if self.tok_id == Id.Eof:
            return []
        else:
            result = self.Sequence()
            if self.tok_id != Id.Eof:
                raise self._Error('Expected EOF')
            #self._Eat(Id.Eof)
            return result

    def Sequence(self):
        """
        A non-empty sequence of commands.

        sequence = cmd (END cmd)* END?
        """
        result = []
        result.append(self.Command())
        while self.tok_id in (Id.Semi, Id.Newline):
            self.End()
            if self.tok_id in (Id.RBrace, Id.Eof):
                break
            result.append(self.Command())

        return result

    def End(self):
        """
        end = semi | newline+
        """
        if self.tok_id == Id.Semi:
            self._Next()
            return

        assert self.tok_id == Id.Newline

        while self.tok_id == Id.Newline:
            self._Next()

    def Block(self):
        """
        block = '{' sequence '}'
        """
        self._Eat(Id.LBrace)
        result = self.Sequence()
        self._Eat(Id.RBrace)
        return result

    def Arg(self):
        """
        arg = word | block
        """
        if self.tok_id == Id.Word:
            val = self.tok_val
            self._Next()
            return val
        if self.tok_id == Id.LBrace:
            return self.Block()
        raise self._Error('Expected argument, got %r' % self.tok_id)

    def Command(self):
        """
        cmd = WORD arg*  # Flexible, uniform syntax
        """
        name = self._Eat(Id.Word)
        args = []
        while self.tok_id in (Id.Word, Id.LBrace):
            args.append(self.Arg())
        #log('ARGS %r', args)

        return name, args

"""
CATBRAIN

stderr:
    log foo    # stderr message - maybe output the R too

stdout:
    flush      # flush() stdout

    w ARG         # write(R) as raw bytes
    rotate ARG    # output rotated version of string
    w-line ARG    # writeline(R)
    w-net

    space
    tab
    newline

    # maybe: w-j8  # j8 string, not JSON

stdin:
    r 3
    r-line
    r-net

    # maybe: w-j8  # j8 string, not JSON

Let other processes use the CPU:

    msleep     # sleep(50 milliseconds)
               # error: not an integer

Heat up the CPU:

    fib        # compute fib(R) and put ASCII representation on the tape
               # error: it's not an integer - print to stderr
    bf <>      # run arbitrary bf program
               # we don't need commands ., but it might be useful for copying
               # and pasting?

I/O
    
    now        # print current time?
    pid        # load PID into register
    signal 12  # send a signal to yourself, or maybe the PID in the register

Encoding:

    to-net     # R = encode(R)
    from-net   # R = decode(R)

GOODBRAIN

    w-file out.txt  # write register to file
    r-file in.txt   # read from file to register

Use memory:

    malloc          # copy the whole tape to a register
    callstack       # use the C call stack (may blow the call stack)

BADBRAIN

    - ubsan - integer behavior
    - asan - overflow
    - syscalls?

Examples:

    # like cat - -f means "forever" or "filter"
    catbrain -f -c 'r 1024;  w'

    # cat, but line-wise
    catbrain -f -c 'r-line;  w-line'

    # repeat 10 times and exit
    catbrain -n 10 -c 'sleep 50; fib 99;  w-line'

    # netstring cat
    catbrain -f -c 'r-line;  to-net;  w-line'

    # throttled
    catbrain -f -c 'r-line; to-net; sleep.100;  w-line'

    # like echo foo
    catbrain -n 1 -c 'const foo;  w-line'

Growth:

    # like seq 3 - write bigger integers
    catbrain -n 3 -c 'add 1;  w-line'

    # writing bigger and bigger lines

    # do we need a 64-bit register for this?
    catbrain -n 3 -c 'const 0; repeat zz; w-line; add 1'

    catbrain -n 3 -c 'const 0; msleep; add 1'

    catbrain -n 3 -c 'const 0; fib; w-line; add 1'

TODO:
    Make sure w-*, r-* don't have Python 3 encoding crap.  I guess use the
    underlying buffer of stdin/stdout.
"""

import optparse
import os
import sys
import subprocess


def log(msg, *args):
    if args:
        msg = msg % args
    print(msg, file=sys.stderr)


class Eof(RuntimeError):
    pass


def Run(prog, state, trace):
    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr

    n = len(prog)

    # catbrain can take the place of:
    #
    # spec/bin
    #   argv.py
    #   stdout_stderr
    #   printenv.py
    #
    # CGI echo
    #   take it over
    #
    # I want to print the env in a readable way?

    for i in range(n):
        command, arg = prog[i]

        # CONDITION
        if command == 'bf':
            prog = arg

            # TODO:
            # Keep (pointer, register) pair
            # . maps to input from register
            # , maps to output

        elif command == 'fib':
            pass

        # STDERR
        elif command == 'log':
            # TODO: expect arg?
            s = arg or '?'

            # output to stderr
            #
            # TODO: could add time?
            stderr.write('  [%d]  #%d  %s\n' % (state['pid'], state['counter'], s))

        # STDOUT
        elif command == 'w':
            s = arg or state['str']
            stdout.write(s)
        elif command == 'w-line':
            s = arg or state['str']
            stdout.write(s)
            stdout.write('\n')

        elif command == 'rotate':
            s = arg or state['str']
            # write rotation based on counter
            r = state['counter'] % len(arg)
            rotated = s[r:] + s[:r]
            stdout.write(rotated)

        elif command == 'space':   # ignore arg?
            stdout.write(' ')
        elif command == 'tab':
            stdout.write('\t')
        elif command == 'newline':
            stdout.write('\n')
        elif command == 'flush':
            stdout.flush()

        ## STDIN
        elif command == 'r-line':
            s = stdin.readline()
            #log('s %r', s)
            if len(s) == 0:
                raise Eof()
            state['str'] = s

        # State
        elif command == 'counter':
            s = str(state['counter'])
            stdout.write(s)

        # PROCESS
        elif command == 'argv':
            s = json.dumps(state['argv'])
            stdout.write(s)
            stdout.write('\n')
        elif command == 'env':
            # Replaces CGI echo?
            # FOO=j'' string might be a better thign
            s = json.dumps(state['env'])
            stdout.write(s)
            stdout.write('\n')
        elif command == 'now':
            # integer seconds
            s = str(int(time.time()))
            stdout.write(s)
        elif command == 'pid':
            s = str(state['pid'])
            stdout.write(s)
        elif command == 'exit':
            code = int(arg)
            sys.exit(code)

        # I/O
        elif command == 'msleep':
            time.sleep(int(arg) / 1000.0)  # milliseconds

        # Loop
        elif command == 'forever':

            body = prog[i+1:]
            while True:
                # Run the rest of the program
                Run(body, state, trace)

        elif command == 'repeat':
            # string to integer conversion is annoying
            iters = int(arg)
            body = prog[i+1:]
            for j in range(iters):
                # Run the rest of the program
                Run(body, state, trace)
            break

        # CONDITION
        elif command == 'cond':
            n = int(arg)

            # If (counter % n == 0), then execute the block
            pass

        else:
            raise RuntimeError('Invalid command %r' % command)

    # Repetitions
    state['counter'] += 1


def Parse(code_str):
    pos = 0
    prog = []

    length = len(code_str)
    while True:
        m = GRAMMAR.match(code_str, pos)
        if not m:
            if pos == length:
                # no more commands
                break
            else:
                raise RuntimeError('Syntax error at %d: %r' % (pos, code_str[pos:]))

        #log('%r', m.groups())
        command, arg, _ = m.groups()
        prog.append((command, arg))

        pos = m.end()

    return prog


class CatBrain(object):
    def __init__(self, argv, env):
        self.step = 0  # iteration counter
        self.str_stack = []  # argv can be pushed here
        self.int_stack = []  # control - loop - conditional to test this?

        self.argv = argv
        self.env = env

    def Run(self, prog):
        pass



def main(argv):
    p = optparse.OptionParser(__doc__)
    p.add_option(
      '-c', dest='command', default='',
      help='program to run')
    p.add_option(
      '-x', dest='trace', action='store_true',
      help='Print debug trace to stderr')
    p.add_option(
      '-n', dest='n', action='store_true',
      help='Parse only')
    p.add_option(
      '-s', dest='str', default='',
      help='Set string register value')

    opts, argv = p.parse_args(argv[1:])

    prog = Parse(opts.command)
    if opts.n:
        log('%s', prog)
        return

    pid = os.getpid()

    state = {
            'pid': pid, 'counter': 0, 'str': opts.str, 'argv': argv, 'env':
            dict(os.environ)}

    try:
        Run(prog, state, opts.trace)
    except Eof:
        # EOF - status is still 0
        pass

    return 0


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
