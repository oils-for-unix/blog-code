#!/usr/bin/env python
# $Id: listsets.py,v 2.1 2004/07/14 17:38:53 zeller Exp $

def listminus(c1, c2):
    """Return a list of all elements of C1 that are not in C2."""
    s2 = {}
    for delta in c2:
        s2[delta] = 1
        
    c = []
    for delta in c1:
        if not s2.has_key(delta):
            c.append(delta)

    return c

def listintersect(c1, c2):
    """Return the common elements of C1 and C2."""
    s2 = {}
    for delta in c2:
        s2[delta] = 1

    c = []
    for delta in c1:
        if s2.has_key(delta):
            c.append(delta)

def listunion(c1, c2):
    """Return the union of C1 and C2."""
    s1 = {}
    for delta in c1:
        s1[delta] = 1

    c = c1[:]
    for delta in c2:
        if not s1.has_key(delta):
            c.append(delta)

    return c

def listsubseteq(c1, c2):
    """Return 1 if C1 is a subset or equal to C2."""
    s2 = {}
    for delta in c2:
        s2[delta] = 1

    for delta in c1:
        if not s2.has_key(delta):
            return 0
