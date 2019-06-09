#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

"""
Find superpermutations with 2-cycle graphs of a particular form.

Uses https://github.com/robinhouston/exactcover
which is a small extension of https://github.com/kwaters/exactcover
"""

import itertools
import sys
from math import factorial

import exactcover

SYMBOLS = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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

class OneCycle(object):
	def __init__(self, start):
		self.cyclerep = cyclerep(start)

	def __str__(self):
		return self.cyclerep

	def __repr__(self):
		return "OneCycle(%r)" % (self.cyclerep,)

	def __eq__(self, other):
		return str(self) == str(other)

	def __hash__(self):
		return hash(str(self))

	def __contains__(self, permutation):
		return self.cyclerep == cyclerep(permutation)

class TwoCycle(object):
	def __init__(self, start):
		self.h = start[-1]
		self.body = start[:-1]

	def __str__(self):
		return "%s/%s" % (self.h, self.body)

	def __repr__(self):
		return "TwoCycle(%r)" % (self.body + self.h,)

	def one_cycles(self):
		for i in range(len(self.body)):
			yield OneCycle(self.body[:i] + self.h + self.body[i:])

class ThreeCycle(object):
	def __init__(self, start):
		self.h1 = start[-1]
		self.h2 = start[-2]
		self.body = start[:-2]

	def __str__(self):
		return "%s/%s/%s" % (self.h1, self.h2, self.body)

	def __repr__(self):
		return "ThreeCycle(%s%s%s)" % (self.body, self.h2, self.h1)

	def two_cycles(self):
		for i in range(len(self.body)):
			yield TwoCycle(self.body[:i] + self.h2 + self.body[i:] + self.h1)

	def one_cycles(self):
		for two_cycle in self.two_cycles():
			for one_cycle in two_cycle.one_cycles():
				yield one_cycle

class PartialTwoCycle(object):
	def __init__(self, two_cycle, i):
		self.two_cycle = two_cycle
		self.i = i

		one_cycles = list(two_cycle.one_cycles())
		self.one_cycles_set = frozenset(one_cycles[: i] + one_cycles[i + 1 :])
		self.omitted_one_cycle = one_cycles[i]

	def entrance(self):
		return rotate(str(self.omitted_one_cycle), self.two_cycle.h)

	def intersection(self, other):
		return self.one_cycles_set.intersection(other)

	def secondary_constraints(self):
		omitted = rotate(str(self.omitted_one_cycle), self.two_cycle.h)
		return (
			"*" + omitted[2 :],
			"*" + omitted[1 : -1]
		)

	def __iter__(self):
		return itertools.chain(self.one_cycles_set, self.secondary_constraints())

	def __contains__(self, other):
		return other in self.one_cycles_set

	def __eq__(self, other):
		return isinstance(other, PartialTwoCycle) and self.one_cycles_set == other.one_cycles_set

	def __hash__(self):
		return hash(self.one_cycles_set)

	def __repr__(self):
		return "PartialTwoCycle(%r, %d)" % (self.two_cycle, self.i)

	def __str__(self):
		return "%s:%d" % (str(self.two_cycle), self.i)

def two_cycles(n):
	for head_index in range(n):
		head = SYMBOLS[head_index]
		body_symbols = SYMBOLS[:head_index] + SYMBOLS[head_index + 1 : n]
		for p in itertools.permutations(body_symbols[1:]):
			yield TwoCycle(body_symbols[0] + "".join(p) + head)

def partial_two_cycles(n):
	for two_cycle in two_cycles(n):
		for i in range(n-1):
			yield PartialTwoCycle(two_cycle, i)

def parse_peloton_spec(spec):
	k = 0
	r = []
	while k < len(spec):
		i = int(spec[k])
		j = 2
		if k + 1 < len(spec) and spec[k + 1] == ' ':
			j = 3
			k += 2
		else:
			k += 1
		r.append((i, j))
	return r


def make_peloton(n, parsed_spec):
	p = SYMBOLS[:n]
	peloton = [p]
	for (pos, (i, j)) in enumerate(parsed_spec):
		for ii in range(i - 1):
			p = p[1:] + p[0]
			peloton.append(p)

		if pos < len(parsed_spec) - 1:
			p = p[j:] + "".join(reversed(p[:j]))
			peloton.append(p)

	return [ OneCycle(p + SYMBOLS[n]) for p in peloton ]

def instance_from_peloton(n, peloton):
	m = []
	secondary = set()
	for partial_two_cycle in partial_two_cycles(n):
		if not partial_two_cycle.intersection(peloton):
			m.append(partial_two_cycle)
			secondary.update(partial_two_cycle.secondary_constraints())

	return (m, secondary)

class BadSolution(Exception):
	def __init__(self, visited):
		super(BadSolution, self).__init__("Bad solution")
		self.visited = visited

def permutations_in_solution(n, peloton, solution):
	entrances = set((
		partial_two_cycle.entrance()
		for partial_two_cycle in solution
	))

	p = SYMBOLS[:n]
	visited = set([p])
	yield p

	peloton_index = 1
	next_one_cycle = peloton[peloton_index]
	return_points = []
	while len(visited) < factorial(n):
		p1 = p[1:] + p[0]
		p2 = p[2:] + p[1] + p[0]
		p3 = p[3:] + p[2] + p[1] + p[0]
		p4 = p[4:] + p[3] + p[2] + p[1] + p[0]

		if p in entrances:
			p = p2
			return_points.append(p1)
		elif p1 not in visited:
			p = p1
		elif len(return_points) == 0 and p2 in next_one_cycle:
			p = p2
			peloton_index += 1
			next_one_cycle = peloton[peloton_index] if peloton_index < len(peloton) else ()
		elif len(return_points) == 0 and p3 in next_one_cycle:
			p = p3
			peloton_index += 1
			next_one_cycle = peloton[peloton_index] if peloton_index < len(peloton) else ()
		elif len(return_points) == 0 and p4 in next_one_cycle:
			p = p4
			peloton_index += 1
			next_one_cycle = peloton[peloton_index] if peloton_index < len(peloton) else ()
		elif len(return_points) > 0 and p2 == return_points[-1]:
			p = p2
			return_points.pop()
		elif p2 not in visited:
			p = p2
		else: raise BadSolution(visited)

		visited.add(p)
		yield p

def squash(p, q):
	if p is None: return q
	if p.endswith(q): return ""
	for i in range(1, len(q)):
		if (p + q[-i :]).endswith(q):
			return q[-i :]

def solution_as_superpermutation(n, peloton, solution):
	s = []
	p = None
	for q in permutations_in_solution(n, peloton, solution):
		s.append(squash(p, q))
		p = q
	return "".join(s)

n = int(sys.argv[1])
peloton_spec = sys.argv[2]
peloton = make_peloton(n-1, parse_peloton_spec(peloton_spec))
matrix, secondary = instance_from_peloton(n, peloton)

all_one_cycles = set()
for partial_two_cycle in matrix:
	all_one_cycles.update(partial_two_cycle.one_cycles_set)


for solution in exactcover.Coverings(matrix, secondary):
	try:
		print solution_as_superpermutation(n, peloton, solution)
	except BadSolution, e:
		# print >>sys.stderr, "BadSolution", e.visited
		pass
# for row in solution: print row
