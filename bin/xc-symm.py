#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

"""
Find superpermutations with 2-cycle graphs of a particular form.

Uses Bogdan Coanda’s symmetries to speed up the search.

Uses https://github.com/robinhouston/exactcover
which is a small extension of https://github.com/kwaters/exactcover
"""

import itertools
import random
import re
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
		self.one_cycles_set = set((
			OneCycle(self.body[:i] + self.h + self.body[i:])
			for i in range(len(self.body))
		))

		n = len(start)
		orbit_generator = {}
		for i in range(n - 2):
			orbit_generator[SYMBOLS[i]] = SYMBOLS[(i + 1) % (n - 2)]

		def apply(mo):
			c = mo.group(0)
			return orbit_generator.get(c, c)

		self.apply_orbit_generator = apply

	def raw_orbit(self, r):
		s = { r }
		n = len(r)
		for i in range(n - 2):
			r = re.sub(r".", self.apply_orbit_generator, r)
			s.add(r)
		return s

	def __str__(self):
		return "%s/%s" % (self.h, self.body)

	def __repr__(self):
		return "TwoCycle(%r)" % (self.body + self.h,)

	def one_cycles(self):
		return self.one_cycles_set

	def intersection(self, other):
		return self.one_cycles_set.intersection(other)

	def orbit(self):
		start = self.body + self.h
		n = len(start)
		r = [ start ]
		for i in range(n - 2):
			start = re.sub(r".", self.apply_orbit_generator, start)
			r.append(start)

		return frozenset(map(TwoCycle, r))

	def partial_two_cycles_not_intersecting(self, one_cycles):
		for i in range(len(self.body)):
			partial_two_cycle = PartialTwoCycle(self, i)
			if not partial_two_cycle.intersection(one_cycles):
				yield partial_two_cycle

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

	def entrances(self):
		return { self.entrance() }

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

class PartialTwoCycleOrbit(object):
	def __init__(self, partial_two_cycles):
		self.one_cycles_set = frozenset.union(*[
			partial_two_cycle.one_cycles_set
			for partial_two_cycle in partial_two_cycles
		])
		self._entrances = [
			partial_two_cycle.entrance()
			for partial_two_cycle in partial_two_cycles
		]
		self._secondary_constraints = sum([
			partial_two_cycle.secondary_constraints()
			for partial_two_cycle in partial_two_cycles
		], ())

	def __iter__(self):
		return iter(self.one_cycles_set)

	def entrances(self):
		return self._entrances

	def secondary_constraints(self):
		return self._secondary_constraints

	def intersection(self, other):
		return self.one_cycles_set.intersection(other)

	def __hash__(self):
		return hash(self.one_cycles_set)

	def __eq__(self, other):
		return isinstance(other, PartialTwoCycleOrbit) and self.one_cycles_set == other.one_cycles_set

	def __contains__(self, other):
		return other in self.one_cycles_set

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

def shuffle(s):
	chars = list(s)
	while True:
		random.shuffle(chars)
		r = "".join(chars)
		if cyclerep(r) != cyclerep(s): return r

def double_3cycle(n):
	"""
	Return an exact cover instance whose solutions represent
	superpermutations with two traversed 3-cycles, and
	the rest of the 2-cycles attached in a tree.
	"""

	m = []
	secondary = set()
	three_cycles = set(ThreeCycle(SYMBOLS[:n]).one_cycles()).union(
		ThreeCycle(SYMBOLS[1:n-3] + SYMBOLS[0] + SYMBOLS[n-3:n]).one_cycles()
	)

	for partial_two_cycle in partial_two_cycles(n):
		if not partial_two_cycle.intersection(three_cycles):
			m.append(partial_two_cycle)
			secondary.update(partial_two_cycle.secondary_constraints())

	return (m, secondary)

def single_4cycle(n):
	"""
	Return an exact cover instance whose solutions represent
	superpermutations with a single traversed 4-cycle, and
	the rest of the 2-cycles attached in a tree.
	"""

	m1, m2 = [], []
	secondary = set()
	three_cycles = set()
	orbits = set()

	a = SYMBOLS[:n-3]
	b = SYMBOLS[n-3:n]
	for i in range(len(a)):
		three_cycles = three_cycles.union(
			ThreeCycle(a[i:] + a[:i] + b).one_cycles()
		)

	for two_cycle in two_cycles(n):
		print >>sys.stderr, ".",
		for partial_two_cycle in two_cycle.partial_two_cycles_not_intersecting(three_cycles):
			m2.append(partial_two_cycle)
			secondary.update(partial_two_cycle.secondary_constraints())

		orbit = two_cycle.orbit()
		if orbit not in orbits:
			orbits.add(orbit)

			for r in itertools.product(*[
				two_cycle.partial_two_cycles_not_intersecting(three_cycles)
				for two_cycle in orbit
			]):
				partial_orbit = PartialTwoCycleOrbit(r)
				m1.append(partial_orbit)
				secondary.update(partial_orbit.secondary_constraints())

	return (m1 + m2, secondary)


class BadSolution(Exception):
	def __init__(self):
		super(BadSolution, self).__init__("Bad solution")

def print_solution(n, solution):
	entrances = set.union(*[
		partial_two_cycle.entrances()
		for partial_two_cycle in solution
	])

	for partial_two_cycle in solution:
		print list(partial_two_cycle)
	p = SYMBOLS[:n]
	visited = set([p])
	print p

	while len(visited) < factorial(n):
		p1 = p[1:] + p[0]
		p2 = p[2:] + p[1] + p[0]
		p3 = p[3:] + p[2] + p[1] + p[0]

		if p in entrances:
			print "-->"
			p = p2
		elif p1 not in visited:
			p = p1
		elif p2 not in visited:
			print "..."
			p = p2
		elif p3 not in visited:
			print "..."
			print "..."
			p = p3
		else: raise BadSolution

		visited.add(p)
		print p

def permutations_in_solution(n, solution):
	entrances = set.union(*[
		partial_two_cycle.entrances()
		for partial_two_cycle in solution
	])

	# print "entrances", entrances

	p = SYMBOLS[:n]
	visited = set([p])
	yield p

	while len(visited) < factorial(n):
		p1 = p[1:] + p[0]
		p2 = p[2:] + p[1] + p[0]
		p3 = p[3:] + p[2] + p[1] + p[0]
		p4 = p[4:] + p[3] + p[2] + p[1] + p[0]

		if p in entrances:
			p = p2
		elif p1 not in visited:
			p = p1
		elif p2 not in visited:
			p = p2
		elif p3 not in visited:
			p = p3
		elif p4 not in visited:
			p = p4
		else: raise BadSolution()

		visited.add(p)
		yield p

def squash(p, q):
	if p is None: return q
	if p.endswith(q): return ""
	for i in range(1, len(q)):
		if (p + q[-i :]).endswith(q):
			return q[-i :]

def solution_as_superpermutation(n, solution):
	s = []
	p = None
	for q in permutations_in_solution(n, solution):
		s.append(squash(p, q))
		p = q
	return "".join(s)

n = int(sys.argv[1])
# matrix, secondary = double_3cycle(n)
matrix, secondary = single_4cycle(n)
# for row in matrix:
# 	print list(row)

print >>sys.stderr, "Searching...";
for solution in exactcover.Coverings(matrix, secondary):
	# print len(solution)
	try:
		print solution_as_superpermutation(n, solution)
	except BadSolution:
		print >>sys.stderr, "Ignoring bad solution"
		pass
# for row in solution: print row
