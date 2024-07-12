#!/usr/bin/env python3
"""
catbrain_test.py: Tests for py_fanos.py
"""
import sys
import unittest
from pprint import pprint

import catbrain  # module under test

Lex = catbrain.Lex

class CatbrainTest(unittest.TestCase):

    def testLexer(self):

        print(Lex(';'))
        print(Lex('foo bar; baz'))
        print(Lex("'foo' 'bar'"))
        print(Lex("if empty { break } "))

        #print(Lex("echo {}"))

        print(Lex("""
        if empty {
          break
        }
        """))

    def testParser(self):
        def _Parse(s):
            print('    case %r' % s)
            tokens = Lex(s)
            #pprint(tokens)

            p = catbrain.Parser(s, tokens)

            #pprint(p.Command())
            #pprint(p.Arg())
            pprint(p.Program())
            print()

        def _ParseError(s):
            try:
                _Parse(s)
            except catbrain.ParseError as e:
                #print('Error: %r' % e.msg)
                print(e)
                pass
            else:
                self.fail('Expected parse error: %r' % s)

        print()
        _ParseError(';')
        _ParseError('{')
        _ParseError('}')

        _ParseError('{spaces-required}')
        _ParseError('a {spaces-required}')
        _ParseError('a spaces-required}')
        _ParseError('<unquoted>')
        _ParseError('space#not comment')

        _ParseError('loop {')
        _ParseError('loop { ')
        _ParseError('loop { }')
        _ParseError('echo ; ;')
        _ParseError('echo hi }')

        # Hm should disallow this, like YSH does
        # I guess we need to understand spaces better?
        # This is similar to a "YSH that's easy to lex" ?
        #_ParseError("echo joined'words'")

        #_ParseError('a')

        # Empty program is valid
        _Parse('')
        _Parse('echo')
        _Parse(' echo;')
        _Parse('\n leading newline # ha')

        _Parse('echo 1 # comment \n \n blank line ok')

        _Parse('echo 1; # comment')
        _Parse('echo a b;')
        _Parse("echo 'foo' 'bar'; echo x y")
        _Parse("echo 'line1'\n echo line2")

        _Parse('if eof { echo yes no }; echo two')

        # This is allowed in catbrain, but not in YSH
        # I guess the default options have no use for it?
        _Parse('my-if { echo yes } { echo no }')

        return

        _Parse('echo 1;exit')
        return


if __name__ == '__main__':
  unittest.main()
