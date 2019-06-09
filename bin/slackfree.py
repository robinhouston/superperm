#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import itertools
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

def slackfree_paths(n, max_num_two_cycles=None):
	p = SYMBOLS[:n]

	permutations = set()
	superpermutation = []
	one_cycles = {}
	two_cycles = {}

	num_permutations = math.factorial(n)

	def search(p, w):
		if p in permutations: return

		one_cycle = cyclerep(p)
		two_cycle = (p[-1], cyclerep(p[:-1]))

		if w > 1:
			two_cycles[two_cycle] = two_cycles.get(two_cycle, 0) + 1
			if max_num_two_cycles is not None and len(two_cycles) > max_num_two_cycles:
				if two_cycles[two_cycle] == 1:
					del two_cycles[two_cycle]
				else:
					two_cycles[two_cycle] -= 1
				return

		permutations.add(p)
		superpermutation.append(p[-w:])
		one_cycles[one_cycle] = one_cycles.get(one_cycle, 0) + 1

		if len(permutations) == num_permutations:
			s = "".join(superpermutation)
			# print "[%d, %d] %r\t%s" % (len(s), len(two_cycles), map(len, superpermutation[1:]), s)
			print "[%d, %d] %s" % (len(s), len(two_cycles), " ".join(superpermutation))

		elif one_cycles[one_cycle] == n:
			search(p[2:] + p[1] + p[0], 2)
			for x in itertools.permutations(p[:3]):
				q = p[3:] + "".join(x)
				if two_cycles.get((q[-1], cyclerep(q[:-1])), 0) == 0:
					search(q, 3)

		else:
			search(p[1:] + p[0], 1)
			if two_cycles.get((p[0], cyclerep(p[1:])), 0) == 0:
				search(p[2:] + p[1] + p[0], 2)

		permutations.remove(p)
		superpermutation.pop()
		one_cycles[one_cycle] -= 1
		if w > 1:
			if two_cycles[two_cycle] == 1:
				del two_cycles[two_cycle]
			else:
				two_cycles[two_cycle] -= 1

	search(SYMBOLS[:n], n)

n = int(sys.argv[1])
if len(sys.argv) == 2:
	slackfree_paths(n)
elif len(sys.argv) == 3:
	max_num_two_cycles = int(sys.argv[2])
	slackfree_paths(n, max_num_two_cycles)
else:
	raise Exception("Wrong number of arguments")
