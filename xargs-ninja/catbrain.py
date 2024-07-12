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
import optparse
import os
import re
import sys
import time


def log(msg, *args):
    if args:
        msg = msg % args
    print(msg, file=sys.stderr)


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

# See catbrain.md
UNQUOTED = r'[a-zA-Z0-9_{}-]+'
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

        sequence = NEWLINE* cmd (END cmd)* END?
        """
        while self.tok_id == Id.Newline:
            self._Next()

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


class Break(RuntimeError):
    pass


class Eof(RuntimeError):
    pass


class CatBrain(object):
    def __init__(self, argv, env):
        self.step = 0  # iteration counter
        self.stack = []  # argv can be pushed here

        self.pid = os.getpid()

        self.stderr = sys.stderr
        self.stdout = sys.stdout
        self.stdin = sys.stdin

        self.argv = argv
        self.env = env

    def _OneArg(self, name, args):
        n = len(args)
        if n == 0:
            arg = self.stack.pop()
        elif n == 1:
            arg = args[0]
        else:
            raise RuntimeError('Command %r got too many args %s' % (name, args))
        return arg

    def Command(self, cmd):
        name, args = cmd

        if name == 'if':
            pass
        elif name == 'loop':
            block = args[0]
            while True:
                try:
                    self.Sequence(block)
                except Break:
                    break

        elif name == 'break':
            raise Break()

        elif name == 'echo':
            s = args[0]
            print(s)

        # STDERR
        elif name == 'log':
            s = self._OneArg(name, args)

            # output to stderr
            #
            # TODO: could add time?
            self.stderr.write('  [%d]  #%d  %s\n' % (self.pid, self.step, s))

        # STDOUT
        elif name == 'w':
            s = self._OneArg(name, args)
            self.stdout.write(s)

        elif name == 'w-line':
            s = self._OneArg(name, args)
            self.stdout.write(s)
            self.stdout.write('\n')

        elif name == 'rotate':
            s = arg or state['str']
            # write rotation based on counter
            r = state['counter'] % len(arg)
            rotated = s[r:] + s[:r]
            stdout.write(rotated)

        elif name == 'space':   # ignore arg?
            stdout.write(' ')
        elif name == 'tab':
            stdout.write('\t')
        elif name == 'newline':
            stdout.write('\n')
        elif name == 'flush':
            stdout.flush()

        ## STDIN
        elif name == 'r-line':
            s = self.stdin.readline()
            #log('s %r', s)
            if len(s) == 0:
                raise Eof()
            self.stack.append(s)

        # State
        elif name == 'counter':
            s = str(state['counter'])
            stdout.write(s)

        # PROCESS
        elif name == 'argv':
            s = json.dumps(state['argv'])
            stdout.write(s)
            stdout.write('\n')
        elif name == 'env':
            # Replaces CGI echo?
            # FOO=j'' string might be a better thign
            s = json.dumps(state['env'])
            stdout.write(s)
            stdout.write('\n')
        elif name == 'now':
            # integer seconds
            s = str(int(time.time()))
            stdout.write(s)
        elif name == 'pid':
            s = str(state['pid'])
            stdout.write(s)
        elif name == 'exit':
            code = int(arg)
            sys.exit(code)

        # I/O
        elif name == 'msleep':
            time.sleep(int(arg) / 1000.0)  # milliseconds

        else:
            raise AssertionError('Invalid command %r' % name)

        self.step += 1

    def Sequence(self, commands):
        for cmd in commands:
            self.Command(cmd)



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

    if 1:
        s = opts.command
        tokens = Lex(s)
        p = Parser(s, tokens)
        prog = p.Program()

        if 0:
            from pprint import pprint
            pprint(prog)

        vm = CatBrain(argv, dict(os.environ))

        # TODO: errors without exceptions?
        try:
            vm.Sequence(prog)
        except Eof:
            # EOF - status is still 0
            pass

        return 0

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
