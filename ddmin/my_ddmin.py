#!/usr/bin/env python
#
# Refactoring / rewrite of original ddmin.py code from Andreas Zeller.

from __future__ import print_function

import re


def listminus(c1, c2):
    """Return a list of all elements of C1 that are not in C2, but in order."""
    s2 = set(c2)
    return [entry for entry in c1 if entry not in s2]


def split(circumstances, n):
    """Split a configuration CIRCUMSTANCES into N subsets;
       return the list of subsets"""

    subsets = []
    start = 0
    for i in range(n):
        len_subset = int((len(circumstances) - start) / float(n - i) + 0.5)
        subset = circumstances[start:start + len_subset]
        subsets.append(subset)
        start += len(subset)

    for s in subsets:
        assert len(s) > 0

    return subsets


def to_string(c):
  return ''.join(char for (_, char) in c)


class Problem(object):

  def __init__(self, s, predicate):
    self.s = s
    self.predicate = predicate
    self.cache = {}  # test string -> bool pass/fail

  def test(self, s, debug_str):
    """Called by ddmin()."""
    if s in self.cache:
        return self.cache[s]

    status = self.predicate(s)

    print("%02i Testing %r %s" % (len(self.cache) + 1, debug_str, 'PASS' if status else 'FAIL'))
    self.cache[s] = status
    return status

  def ddmin(self):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""

    orig_length = len(self.s)

    assert self.test('', '.' * orig_length)
    assert not self.test(self.s, self.s)

    circumstances = list(enumerate(self.s))
    orig_length = len(self.s)

    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)

        some_complement_is_failing = False
        for subset in subsets:
            complement = listminus(circumstances, subset)

            s = to_string(complement)
            lookup = dict(complement)
            debug_str = ''.join(lookup.get(i, '.') for i in range(orig_length))

            if not p.test(s, debug_str):
                circumstances = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    return to_string(circumstances)


if __name__ == "__main__":
    s = '<SELECT NAME="priority" MULTIPLE SIZE=7>'
    predicate = lambda x: not re.match("<SELECT.*>", x)
    #predicate = lambda x: not re.search("MUL.*>", x)
    p = Problem(s, predicate)

    solution = p.ddmin()
    print('')
    print(solution)
