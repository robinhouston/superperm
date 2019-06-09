#!/usr/bin/python
# -*- encoding: UTF8 -*-

"""
Generate a universal cycle on n symbols, i.e. a circular string S of length n! symbols in which every
sequence of (n-1) distinct symbols appears as an (n-1)-character substring.

Frank Ruskey and Aaron Williams. 2010. An explicit universal cycle for the (n-1)-permutations of an n-set.
ACM Trans. Algorithms 6, 3, Article 45 (July 2010), 12 pages. DOI: https://doi.org/10.1145/1798596.1798598
"""

import sys

SYMBOLS = "123456789ABCDEFG"


n = int(sys.argv[1])

def intersperse(a, b):
	"""Alternate between copies of a and elements of b"""
	return sum([a + [e] for e in b], [])

def S(i):
	if i < 2: raise Exception(u"Must have n ≥ 2")
	if i == 2: return [False, False]
	return intersperse([False, False] + [True] * (i-3), [ not e for e in S(i-1) ])

s = SYMBOLS[:n]
r = ""
for b in S(n):
	r += s[0]
	if b: s = s[1:-1] + s[0] + s[-1]
	else: s = s[1:] + s[0]

print r
