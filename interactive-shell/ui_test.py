#!/usr/bin/python -S
"""
ui_test.py: Tests for ui.py
"""
from __future__ import print_function

import unittest

import ui  # module under test


# TODO: Unit tests should test some properties of the output!
# How many lines are there, and did it overflow?

class VisualTest(unittest.TestCase):

  def testPrintPacked(self):
    matches = ['foo', 'bar', 'spam', 'eggs', 'python', 'perl']
    longest_match_len = max(len(m) for m in matches)
    for width in (10, 20, 30, 40, 50):
      n = ui.PrintPacked(matches, longest_match_len, width, 10)
      print('Wrote %d lines' % n)
      print('')

  def testTooMany(self):
    matches = ['--flag%d' % i for i in xrange(100)]
    longest_match_len = max(len(m) for m in matches)
    for width in (10, 20, 30, 40, 50, 60):
      n = ui.PrintPacked(matches, longest_match_len, width, 10)
      print('Wrote %d lines' % n)
      print('')


class UiTest(unittest.TestCase):

  def testNiceDisplay(self):
    comp_state = {}

    display = ui.NiceDisplay(comp_state, bold_line=False)
    # This one is important
    display.EraseLines()
    display.Reset()
    display.SetPromptLength(10)

    # These are related but we can just set them separately.
    comp_state['ORIG'] = 'echo '  # for returning to the prompt
    comp_state['prefix_pos'] = 5  # Strip this off every candidate

    display.PrintMessage('hello')

    matches = ['echo one', 'echo two']
    display.PrintCandidates(None, matches, None)

    display.OnWindowChange()

    # This needs to be aware of the terminal width.
    # It's a bit odd since it's called as a side effect of the PromptEvaluator.
    # That class knows about styles and so forth.

    display.ShowPromptOnRight('RIGHT')


if __name__ == '__main__':
  unittest.main()
