#!/usr/bin/env python3
from __future__ import print_function
"""
catbrain - Embedded language like shell, Tcl, Forth, jq

See README.md
"""

import io
import json
import optparse
import os
import re
import subprocess
import sys
import time


def log(msg, *args):
    if args:
        msg = msg % args
    print(msg, file=sys.stderr)


class ParseError(RuntimeError):
    pass


# See README.md
UNQUOTED = r'[a-zA-Z0-9_/.-]+'  # /. for filenames
LBRACE = r'{'
RBRACE = r'}'
SQ = r"'[^']*'"
SEMI = r';'
NEWLINE = r'[\n]'

# Ignored tokens
SPACE = r'[ ]'
COMMENT = r'#[^\n]*'

# Comment must come before space
TOKENS = [UNQUOTED, LBRACE, RBRACE, SQ, SEMI, NEWLINE, COMMENT, SPACE]

LEXER_RE = re.compile('|'.join('(%s)' % pat for pat in TOKENS))


class Id:
    Word = 'w'
    Semi = ';'
    Newline = 'n'
    LBrace = '{'
    RBrace = '}'

    Eof = ''  # For parser

    # Not seen by the parser
    Comment = '#'
    Space = 's'


def Lex(code_str):
    tokens = []

    pos = 0
    n = len(code_str)

    # Enforce shell-like rule:
    #
    # - Semi and Newline are "operator tokens"
    # - Word, LBrace, RBrace are "word tokens"
    #   - they must be followed by: space, newline, eof
    #   - equivalently: they must be preceded by: space, newline, semi, BEGINNING
    #     of file
    # - comments must also be preceded by separator
    saw_separator = True

    while pos != n:
        m = LEXER_RE.match(code_str, pos)
        if not m:
            raise ParseError('Invalid token at %r' % code_str[pos:pos+10])
        unquoted, lbrace, rbrace, sq, semi, newline, comment, space = m.groups()
        #print(m.groups())

        token = None
        if unquoted is not None:
            token = (Id.Word, unquoted)

        elif lbrace is not None:
            token = (Id.LBrace, None)

        elif rbrace is not None:
            token = (Id.RBrace, None)

        elif sq is not None:
            token = (Id.Word, sq[1:-1])

        elif semi is not None:
            token = (Id.Semi, semi)

        elif newline is not None:
            token = (Id.Newline, newline)

        elif space is not None:
            token = (Id.Space, None)

        elif comment is not None:
            token = (Id.Comment, None)

        else:
            raise AssertionError()

        tok_id, tok_val = token

        if tok_id in (Id.Word, Id.LBrace, Id.RBrace, Id.Comment):
            if not saw_separator:
                raise ParseError('Expected separator before token %r %r'
                                 % (token, code_str[pos:pos+10]))

        # Update it for next iteration
        saw_separator = tok_id in (Id.Space, Id.Newline, Id.Semi)

        if tok_id not in (Id.Space, Id.Comment):
            token_len = len(m.group(0))
            tokens.append((tok_id, tok_val, pos, token_len))

        pos = m.end()

    tokens.append((Id.Eof, None, pos, 0))
    return tokens


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
        program = Eof | seq Eof
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

        seq = NEWLINE* cmd (terminator cmd)* terminator?
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
        terminator = semi | newline+
        """
        if self.tok_id == Id.Semi:
            self._Next()
            return

        assert self.tok_id == Id.Newline

        while self.tok_id == Id.Newline:
            self._Next()

    def Block(self):
        """
        block = '{' seq '}'
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
        # Flexible, uniform syntax
        cmd = WORD arg*
        """
        name = self._Eat(Id.Word)
        args = []
        while self.tok_id in (Id.Word, Id.LBrace):
            args.append(self.Arg())
        #log('ARGS %r', args)

        return name, args


class Break(RuntimeError):
    pass


class ctx_Output(object):
    def __init__(self, vm):
        self.vm = vm
        self.old_stdout = vm.stdout
        vm.stdout = io.StringIO()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        # String
        self.vm.stack.append(self.vm.stdout.getvalue())
        self.vm.stdout = self.old_stdout


class ctx_Input(object):
    def __init__(self, vm):
        self.vm = vm
        self.old_stdin = vm.stdin
        top = self.vm.stack.pop()
        vm.stdin = io.StringIO(top)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.vm.stdin = self.old_stdin


class ctx_TopArray(object):
    def __init__(self, vm):
        self.vm = vm

        new_array = []
        self.old_stack = vm.stack
        self.old_stack.append(new_array)

        vm.stack = new_array

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.vm.stack = self.old_stack


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

        self.defs = {}

    def _BlockArg(self, name, args):
        n = len(args)
        if n != 1:
            raise RuntimeError('Command %r expected one arg, got %d' % (name, n))
        arg = args[0]
        if not isinstance(arg, list):
            raise RuntimeError('Command %r expected block arg, got %s' % (name, arg))
        return arg

    def _OneArg(self, name, args):
        n = len(args)
        if n == 0:
            arg = self.stack.pop()
        elif n == 1:
            arg = args[0]
        else:
            raise RuntimeError('Command %r got too many args %s' % (name, args))

        return arg

    def _DataArg(self, name, args):
        """
        We have two styles:

            w          # take arg from the stack
            w foo      # take arg from immediate

        This is a runtime error

           w foo bar  # BAD
        """
        arg = self._OneArg(name, args)
        if not isinstance(arg, str):
            raise RuntimeError('Expected str, got %s' % arg)
        return arg

    def _ArgArray(self, name, args):
        """
        Styles:
          # take array of args from immediate
          extern ls _tmp

          const-array ls /tmp
          extern
        """
        n = len(args)
        if n == 0:
            array = self.stack.pop()
        else:
            array = args
        if not isinstance(array, list):
            raise RuntimeError('Expected list, got %s' % array)
        return array

    def Command(self, cmd):
        name, args = cmd

        # Everything can be redefined?  Even if and def?
        body = self.defs.get(name)
        if body is not None:
            # Push args!
            self.stack.extend(args)

            # TODO: what's the status?
            self.Sequence(body)
            return 0

        # CONTROL FLOW
        if name == 'def':
            name = args[0]
            body = args[1]

            self.defs[name] = body

        elif name == 'if':
            # if empty { w-line hi }
            # could also be:
            # if predicate a b { w-line hi }
            pred_name = args[0]
            block = args[1]

            pred_cmd = (pred_name, [])

            # Does every command have an integer status?
            status = self.Command(pred_cmd)
            if status == 0:
                self.Sequence(block)

        elif name == 'loop':  # not in catbrain, only nullbrain and shbrain
            block = args[0]
            while True:
                try:
                    self.Sequence(block)
                except Break:
                    break

        elif name == 'break':
            raise Break()

        elif name == 'for':
            # Assume the TOS is list, and iterate over it
            raise NotImplementedError()

        elif name == 'for-line':
            # cat-like loop of: r-line w
            raise NotImplementedError()

        elif name == 'feed':
            block = self._BlockArg(name, args)

            with ctx_Input(self):
                self.Sequence(block)

        elif name == 'capture':
            block = self._BlockArg(name, args)

            with ctx_Output(self):
                self.Sequence(block)

        elif name == 'array':
            block = self._BlockArg(name, args)

            with ctx_TopArray(self):
                self.Sequence(block)

        elif name == 'eval':
            block = self._BlockArg(name, args)
            self.Sequence(block)

        # MANIPULATE STACK
        elif name == 'const':  # push constant
            s = args[0]
            self.stack.append(s)

        elif name == 'const-array':  # push constant
            self.stack.append(args)

        elif name == 'gather':
            # replace the stack with an array
            self.stack = [self.stack]

        elif name == 'spread':  # spread the top array out
            top = self.stack.pop()
            if not isinstance(top, list):
                raise RuntimeError('spread expects a list, got %r' % top)
            self.stack.extend(top)

        elif name == 'join':
            # this is a bit 'spread'
            top = self.stack.pop()
            self.stack.append(''.join(top))

        elif name == 'dup':
            top = self.stack[-1]
            self.stack.append(top)

        elif name == 'pop':
            n = len(args)
            if n == 0:
                p = 1
            elif n == 1:
                p = int(args[0])
            else:
                raise RuntimeError('Pop expected 1 arg, got %s' % n)

            for i in range(p):
                self.stack.pop()

        elif name == 'empty-stack':
            # Result is empty?
            if len(self.stack) == 0:
                return 0
            else:
                return 1

        elif name == 'empty-string':
            top = self.stack[-1]
            if len(top) == 0:
                return 0
            else:
                return 1

        elif name == 'is-zero':
            top = self.stack[-1]
            if top == '0':
                return 0
            else:
                return 1

        elif name == 'ch':   # ignore arg?
            what = args[0]
            if what == 'space':
                ch = ' '
            elif what == 'tab':
                ch = '\t'
            elif what == 'newline':
                ch = '\n'
            else:
                raise AssertionError()

            self.stack.append(ch)

        # STDERR
        elif name == 'log':
            s = self._DataArg(name, args)

            # output to stderr
            #
            # TODO: could add time?
            self.stderr.write('  [%d]  #%d  %s\n' % (self.pid, self.step, s))

        elif name == 'pp':
            what = args[0]
            if what == 'top':
                value = self.stack[-1]
                self.stderr.write('  #%d  top = %r\n' % (self.step, value))
            elif what == 'stack':
                self.stderr.write('  #%d  stack = %r\n' % (self.step, self.stack))
            else:
                raise AssertionError(what)

        # STDOUT
        elif name == 'w':
            s = self._DataArg(name, args)
            self.stdout.write(s)

        elif name == 'w-line':
            s = self._DataArg(name, args)
            self.stdout.write(s)
            self.stdout.write('\n')

        elif name == 'flush':
            self.stdout.flush()

        ## STDIN
        elif name == 'r':
            n = int(args[0])
            s = self.stdin.read(n)
            self.stack.append(s)

        elif name == 'r-line':
            s = self.stdin.readline()
            self.stack.append(s)

        # STATE
        elif name == 'load':
            what = self._DataArg(name, args)
            if what == 'argv':
                self.stack.extend(self.argv)
            elif what == 'env':
                strs = ['%s=%s' % (k, v) for k, v in os.environ.items()]
                self.stack.extend(strs)
            elif what == 'counter':
                s = str(self.step)
                self.stack.append(s)
            elif what == 'now':
                # integer seconds
                s = str(int(time.time()))
                self.stack.append(s)
            elif what == 'pid':
                s = str(self.pid)
                self.stack.append(s)
            else:
                raise AssertionError(what)

        # COMPUTE

        # TODO:
        # - bf
        # - fib
        elif name == 'op':
            how = args[0]
            s = self.stack.pop()
            if how == 'rotate':
                # write rotation based on counter
                r = self.step % len(s)
                rotated = s[r:] + s[:r]
                self.stack.append(rotated)
            elif how == 'dec':
                m = str(int(s) - 1)
                self.stack.append(m)
            else:
                raise AssertionError(how)

        # FORMATS
        elif name == 'encode':
            fmt = args[0]
            if fmt == 'json':
                s = self.stack.pop()
                self.stack.append(json.dumps(s))
            elif fmt == 'j8':  # must be string I think
                raise NotImplementedError()
            elif fmt == 'netstr':
                raise NotImplementedError()
            else:
                raise NotImplementedError()

        elif name == 'decode':
            fmt = args[0]
            if fmt == 'json':
                s = self.stack.pop()
                self.stack.append(json.loads(s))
            elif fmt == 'j8':
                raise NotImplementedError()
            elif fmt == 'netstr':
                raise NotImplementedError()
            else:
                raise NotImplementedError()

        elif name == 'exit':
            s = self._DataArg(name, args)
            code = int(s)
            sys.exit(code)

        # I/O
        elif name == 'msleep':
            s = self._DataArg(name, args)
            time.sleep(int(s) / 1000.0)  # milliseconds

        elif name == 'extern':
            arg_array = self._ArgArray(name, args)

            log('EX %s', arg_array)

            # Hm, we should get these from the STACK too!
            status = subprocess.call(arg_array)
            return status

        elif name == 'sh':
            arg = self._DataArg(name, args)
            status = subprocess.call(['sh', '-c', arg])
            return status

        else:
            raise AssertionError('Invalid command %r' % name)

        self.step += 1

        return 0

    def Sequence(self, commands):
        for cmd in commands:
            status = self.Command(cmd)
            if status != 0:
                raise RuntimeError('Command failed with status %d' % status)


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

    s = opts.command
    tokens = Lex(s)
    p = Parser(s, tokens)
    prog = p.Program()

    if 0:
        from pprint import pprint
        pprint(prog)

    vm = CatBrain(argv, dict(os.environ))

    # TODO: errors without exceptions?
    vm.Sequence(prog)

    return 0


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
