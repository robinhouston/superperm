#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import math
import sys

SYMBOLS = "123456789ABCDEFG"

def rotate(w, x):
	"""
	Rotate the word w so it starts with the symbol x.
	"""
	i = w.index(x)
	return w[i:] + w[:i]

def cyclerep(w):
	"""
	The canonical representative of the cyclic equivalence class of w,
	assuming w has no repeated symbols.
	"""
	return rotate(w, min(w))

def is_valid(n, peloton):
	p = SYMBOLS[:n]

	c = cyclerep(p)
	one_cycles = set([c])

	i = peloton[0]
	if i == 0: return False
	exit = p[i-1:] + p[:i-1]

	for i in peloton[1:]:
		if i == 0:
			exit = exit[:2] + exit[3:] + exit[2]
		else:
			p = exit[2:] + exit[1] + exit[0]
			c = cyclerep(p)
			if c in one_cycles: return False
			one_cycles.add(c)
			exit = p[i-1:] + p[:i-1]

	return True

def score(n, peloton):
	return sum(peloton) - (n-1) * len(peloton)

def find_palindromes(n):
	def search(a=[]):
		if len(a) > 0:
			if not is_valid(n, a + [1]) and not is_valid(n, a + [0, 1]): return
			if sum(a) + (15 - len(a)) < (n - 1): return
			yield a + list(reversed(a))
			yield a + list(reversed(a[:-1]))

		if len(a) >= 15: return
		for i in (7,5): # range(n, -1, -1):
			for peloton in search(a + [i]): yield peloton

	for peloton in search():
		if sum(peloton) % (n-1) != 0: continue
		s = score(n, peloton)
		if s <= n-1: continue
		if not is_valid(n, peloton): continue
		print("{}: {}".format(s, "".join([ " " if x == 0 else str(x) for x in peloton ])))


n = int(sys.argv[1])
find_palindromes(n)
