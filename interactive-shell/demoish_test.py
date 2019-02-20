#!/usr/bin/python -S
"""
demoish_test.py: Tests for demoish.py
"""
from __future__ import print_function

import unittest

import ui
import demoish  # module under test


class DemoishTest(unittest.TestCase):

  def testRootCompleter(self):
    comp_state = {}
    comp_lookup = {
        'echo': demoish.WordsAction(['foo', 'bar']),
    }
    display = ui.NiceDisplay(comp_state, bold_line=True)
    prompt = demoish.PromptEvaluator(demoish._RIGHT, display)
    reader = demoish.InteractiveLineReader('$ ', '> ', prompt, display)
    reader.pending_lines.extend([
        'echo \\\n',  # first line
    ])

    r = demoish.RootCompleter(reader, display, comp_lookup, comp_state)
    # second line
    matches = list(r.Matches({'line': 'x f'}))
    print(matches)

    # this is what readline wants
    self.assertEqual(['x foo '], matches)

  def testMakeCompletionRequest(self):
    f = demoish.MakeCompletionRequest
    # complete the first word
    self.assertEqual((None, 'ech', '', 0), f(['ech']))

    # complete argument to echo
    self.assertEqual(('echo', '', 'echo ', 5), f(['echo ']))
    self.assertEqual(('echo', 'f', 'echo ', 5), f(['echo f']))

    # CAN complete this
    self.assertEqual(('echo', '', '', 0), f(['echo \\\n', '']))

    # can't complete a first word split over multiple lines without space
    self.assertEqual(-1, f(['ec\\\n', 'ho']))

    # can't complete a first word split over multiple lines with space
    self.assertEqual(-1, f(['ec\\\n', 'ho f']))

    # can't complete last word split over multiple lines
    self.assertEqual(-2, f(['echo f\\\n', 'o']))

    # CAN complete with line break in the middle
    self.assertEqual(('echo', 'b', 'oo ', 3), f(['echo f\\\n', 'oo b']))

  def testCompletionCallback(self):
    pass

  # The display manages the details of drawing:
  # - the terminal width
  # - the prompt length

  # So we could have a NiceDisplay and a BasicDisplay?
  # The BareDisplay is like readline's default.


    
if __name__ == '__main__':
  unittest.main()
