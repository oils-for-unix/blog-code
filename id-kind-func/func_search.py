#!/usr/bin/env python3
"""
func_search.py -- Search for functions to replace a lookup table.

See http://www.oilshell.org/blog/2016/12/23.html
"""

from collections import Counter, defaultdict
import inspect
import json
import sys


DESIRED_DIST = sorted([1, 1, 3, 3, 1, 15, 12, 10, 11, 12, 10, 8, 8, 4, 43, 20, 1, 16, 4, 25, 13], reverse=True)


def ik1(tok):
  return tok & (-tok - 23)


def ik2(tok):
  return (tok & 230) & (tok + 13)


def ik3(tok):
  return 12 | tok | (tok + 15)


def ik4(tok):
  return (tok + 108) | (tok ^ 163) 


def ik5(tok):
  return (tok ^ 35) & (tok + 20)


def ik6(tok):
  return (12 -tok) & (tok ^ 6) & (tok + 14)


def ik7(tok):
  return 175 & tok & ((tok ^ 173) + 11)


# Blog post code

def LookupKind1(id):
  kind = id & (-id - 23)
  if kind:      return kind
  if id <= 1:   return 20
  if id <= 9:   return 44
  if id <= 40:  return 48
  if id <= 72:  return 50
  if id <= 105: return 4
  return 2

def LookupKind2(id):
  return (id & 230) & (id + 13) if id else 32


def Deficit(want, need):
  n = min(len(want), len(need))
  deficit = []
  for i in range(n):
    d = need[i] - want[i]
    deficit.append(d if d < 0 else 0)
  return deficit


def Show(label, a):
  sys.stdout.write('%12s' % label)
  print(''.join('%5d' % item for item in a))


def Hist(f):
  h = Counter(f(tok) for tok in range(256))
  pairs = sorted(h.items(), key=lambda p: p[1], reverse=True)
  return pairs


def FunctionBody(f):
  lines, _ = inspect.getsourcelines(f)
  return lines[1]


def TestFunc(f):
  """See if a given function has the desired distribution of return values."""
  print(f)
  print(FunctionBody(f))

  hist = Hist(f)
  #print(hist)
  #if any(k > 255 for k in hist.keys()):
  #  raise AssertionError('OUT OF RANGE')

  # Compare the two
  # TODO: sort in the same order?
  Show('func range', [result for result, _ in hist])
  #pad = [0] * offset
  pad = []
  want = pad + DESIRED_DIST
  need = [freq for _, freq in hist]

  d = Deficit(want, need)

  Show('want dist', want)
  Show('have dist', need)
  Show('deficit', d)

  print('Unique values:', len(hist))
  print()


def NumDeficits(dist, desired_dist):
  """Return the number of kinds that are too small.

  Args:
    dist: array sorted in reverse order
    desired_dist: ditto
  """
  #need = set(desired_dist)
  n = len(desired_dist)
  num_deficits = 0
  for i in range(n):
    if dist[i] < desired_dist[i]:
      num_deficits += 1
  return num_deficits


def ScoreFunction(hist):
  func_range_size = len(hist)
  if func_range_size < 21:
    #print('%d - %d values not enough' % (i, func_range_size))
    return

  dist = [freq for _, freq in hist]
  func_range = [result for result, _ in hist]
  if any(v > 255 for v in func_range):
    #print('%d - %d is too big' % (0, max(func_range)))
    return
  if any(v < 0 for v in func_range):
    #print('%d - %d is too small' % (0, min(func_range)))
    return

  num_deficits = NumDeficits(dist, DESIRED_DIST)
  #print('n = %d, deficit %d' % (i, deficit))
  if num_deficits <= 1:
    print('Kind that are too small: %d' % num_deficits)
    d = Deficit(DESIRED_DIST, dist)

    Show('func range', func_range)
    Show('want dist', DESIRED_DIST)
    Show('have dist', dist)
    Show('deficit', d)

  return num_deficits


def f1(tok, n):
  return tok & (-tok - n)

def g1(tok, n):
  return tok & (tok - n)


def Form1(f):
  #return
  min_deficit = 256
  for i in range(256):
    #hist = Hist(lambda tok: f(tok, i))
    hist = Hist(lambda tok: f(tok, i))
    num_deficits = ScoreFunction(hist)
    if num_deficits is not None:
      min_deficit = min(min_deficit, num_deficits)
  print('Min deficit: %d'% min_deficit)



def f2_1(tok, i, j):
  return (tok & i) & (tok + j)

def f2_2(tok, i, j):
  return (tok ^ i) & (tok + j)

# This is horrible
def f2_3(tok, i, j):
  return (tok ^ i) & (tok & j)

# This is bad too -- most are too big
def f2_4(tok, i, j):
  return (tok + i) & (tok - j)

# min deficit: 3
def f2_5(tok, i, j):
  return (tok | i) & (tok + j)

# These are all bad.  minimum 11 deficits!

def f2_6(tok, i, j):
  return (tok | i) & (tok | j)
def f2_7(tok, i, j):
  return (tok & i) | (tok & j)
def f2_8(tok, i, j):
  return (tok ^ i) & (tok ^ j)

# not bad, but not good.  min deficit 2
def f2_9(tok, i, j):
  return (tok & i) ^ (-tok - j)

def f2_10(tok, i, j):
  return (tok & i) ^ (-tok & j)

def f2_11(tok, i, j):
  return (i - tok) & (j - tok)

def f2_12(tok, i, j):
  return (i - tok) | (j - tok)

# Too many negative results
def f2_13(tok, i, j):
  return i | tok | (j - tok)

# Doesn't work either
def f2_14(tok, i, j):
  return - (i | tok | (j - tok))

def f2_15(tok, i, j):
  return (i & tok) & (tok | j)

def f2_16(tok, i, j):
  return (tok ^ i) & (tok | j)


#
# Functions involving shifts
#

def f3_1(tok, s, j):
  return (tok >> s) & (- j - tok)

def f3_2(tok, s, j):
  return (tok >> s) & (tok - j)

def f3_3(tok, s, j):
  return (tok >> s) & (tok + j)

def f3_4(tok, s, j):
  return (tok >> s) & (tok ^ j)

def f3_5(tok, s, j):
  return (tok >> s) & (tok | j)

def f3_6(tok, s, j):
  return (tok | j) >> s
def f3_7(tok, s, j):
  return (tok & j) >> s
def f3_8(tok, s, j):
  return (tok ^ j) >> s


def Form2(f):
  #return
  deficit1 = 0
  min_deficit = 256
  for i in range(256):
    for j in range(256):
      #hist = Hist(lambda tok: f(tok, i))
      hist = Hist(lambda tok: f(tok, i, j))
      num_deficits = ScoreFunction(hist)
      if num_deficits == 1:
        deficit1 += 1
        print('i = %d, j = %d' % (i, j))
      if num_deficits is not None:
        min_deficit = min(min_deficit, num_deficits)
  print('Min deficit: %d' % min_deficit)
  print('number of solutions with a deficit of 1: %d' % deficit1)


def Form3(f):
  #return
  deficit1 = 0
  min_deficit = 256
  for s in range(8):
    for j in range(256):
      #hist = Hist(lambda tok: f(tok, i))
      hist = Hist(lambda tok: f(tok, s, j))
      num_deficits = ScoreFunction(hist)
      if num_deficits == 1:
        deficit1 += 1
        print('i = %d, j = %d' % (s, j))
      if num_deficits is not None:
        min_deficit = min(min_deficit, num_deficits)
  print('Min deficit: %d' % min_deficit)
  print('number of solutions with a deficit of 1: %d' % deficit1)


def f4_1(tok, i, j, k):
  return (tok ^ i) & (tok + j) & (tok + k)

def f4_2(tok, i, j, k):
  return (tok ^ i) & (tok ^ j) & (tok + k)

# FOUND A deficit of 1 here!  (Actually 12 of them)
def f4_3(tok, i, j, k):
  return (-tok + i) & (tok + j) & (tok + k)

def f4_4(tok, i, j, k):
  return (-tok + i) & (-tok + j) & (tok + k)

# WOWWWW
# num deficits 0, i = 12, j = 6, k = 14

# Mysterious.
#
# (-tok + 12) & (tok ^ 6) & (tok + 14)

def f4_5(tok, i, j, k):
  return (-tok + i) & (tok ^ j) & (tok + k)


def Form4(f):
  deficit1 = 0
  min_deficit = 256
  # 2^5 bits * 3 -- less than 2^8 * 2
  for i in range(-16, 16):
    for j in range(-16, 16):
      for k in range(-16, 16):
        hist = Hist(lambda tok: f(tok, i, j, k))
        num_deficits = ScoreFunction(hist)
        if num_deficits == 1:
          deficit1 += 1
        if num_deficits in (0, 1):
          print('num deficits %d, i = %d, j = %d, k = %d' % (num_deficits, i, j, k))
          print('')
        if num_deficits == 0:
          raise RuntimeError('Found exact solution')
        if num_deficits is not None:
          min_deficit = min(min_deficit, num_deficits)

  print('Min deficit: %d' % min_deficit)
  print('number of solutions with a deficit of 1: %d' % deficit1)


def Search():
  print(sorted(DESIRED_DIST))
  print(sum(DESIRED_DIST))
  print('-'* 70)

  # ik3 and ik4 are out of range
  TestFunc(ik1)
  TestFunc(ik2)
  TestFunc(ik5)
  TestFunc(ik6)
  TestFunc(ik7)
  TestFunc(LookupKind1)
  TestFunc(LookupKind2)

  Form1(f1)
  Form1(g1)

  #Form2(f2)
  #Form2(g2)
  #Form2(h2)  BAD
  #Form2(j2)
  #Form2(f2_1)
  #Form2(f2_6)
  #Form2(f2_7)
  #Form2(f2_8)

  #Form2(f2_9)
  #Form2(f2_10)
  #Form2(f2_11)
  #Form2(f2_12)
  #Form2(f2_16)

  #Form3(f3_1)
  #Form3(f3_2)
  #Form3(f3_5)

  #Form3(f3_6)
  #Form3(f3_7)
  #Form3(f3_8)

  #Form4(f4_3)  # DEFICIT 1
  #Form4(f4_4)
  # EXACT ONE
  Form4(f4_5)

  # Then search for functions with a similar distribution?


def PrintSolution(name):
  f = getattr(sys.modules[__name__], name)
  #print(FunctionBody(f))
  hist = defaultdict(list)
  for i in range(256):
    k = f(i)
    hist[k].append(i)

  solution = {}
  items = sorted(hist.items(), key=lambda p: len(p[1]), reverse=True)

  # TODO: Assign it to desired_dist

  i = 0
  for k, id_list in items:
    d = DESIRED_DIST[i] if i < len(DESIRED_DIST) else 0
    print(d, ':', len(id_list), 'ids-of-kind', k, ':',
          ' '.join(str(i) for i in id_list))
    i += 1

  #json.dump(solution, sys.stdout, indent=None)


def main(argv):
  action = argv[1]
  if action == 'search':
    Search()
  elif action == 'print':
    PrintSolution(argv[2])


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('ABORT: %s' % e, file=sys.stderr)
    sys.exit(1)
