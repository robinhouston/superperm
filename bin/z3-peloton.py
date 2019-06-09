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

import z3

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

def one_cycles(n):
	for p in itertools.permutations(SYMBOLS[1:n]):
		yield OneCycle(SYMBOLS[0] + "".join(p))

def two_cycles(n):
	for head_index in range(n):
		head = SYMBOLS[head_index]
		body_symbols = SYMBOLS[:head_index] + SYMBOLS[head_index + 1 : n]
		for p in itertools.permutations(body_symbols[1:]):
			yield TwoCycle(body_symbols[0] + "".join(p) + head)

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
		for ii in range(i-1):
			p = p[1:] + p[0]
			peloton.append(p)

		if pos < len(parsed_spec) - 1:
			p = p[j:] + "".join(reversed(p[:j]))
			peloton.append(p)

	return [ OneCycle(p + SYMBOLS[n]) for p in peloton ]

def instance_from_peloton(n, peloton):
	n_one_cycles = factorial(n-1)
	n_two_cycles = (n_one_cycles - len(peloton)) // (n-2)

	one_cycle_index = {}
	for (i, one_cycle) in enumerate(one_cycles(n)):
		one_cycle_index[one_cycle] = i

	solver = z3.Goal()
	bv_two_cycles = [
		z3.BitVec("two_cycle_%d" % i, n_one_cycles)
		for i in range(n_two_cycles + 1)
	]
	bv_cumulative = [
		z3.BitVec("cumu_%d" % i, n_one_cycles)
		for i in range(n_two_cycles + 1)
	]

	def one_cycles_bv(one_cycles):
		bv = 0L
		for one_cycle in one_cycles:
			bv |= 1 << one_cycle_index[one_cycle]
		return bv

	bv_peloton = one_cycles_bv(peloton)
	solver.add(bv_cumulative[0] == bv_peloton)
	solver.add(bv_two_cycles[0] == bv_peloton)

	two_cycles_list = [
		one_cycles_bv(two_cycle.one_cycles())
		for two_cycle in two_cycles(n)
	]

	def is_two_cycle(bv):
		return reduce(lambda condition, two_cycle_bv: z3.Or(condition, bv == two_cycle_bv), two_cycles_list, False)

	for i in range(1, n_two_cycles + 1):
		solver.add(is_two_cycle(bv_two_cycles[i]))
		solver.add(bv_cumulative[i] == (bv_cumulative[i-1] | bv_two_cycles[i]))

		overlap = bv_cumulative[i-1] & bv_two_cycles[i]
		solver.add(overlap != 0)
		solver.add(overlap & (overlap - 1) == 0)

	return solver

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
solver = instance_from_peloton(n, peloton)

tactic = z3.Then("simplify", "bit-blast", "tseitin-cnf")
subgoal = tactic(solver)
assert len(subgoal) == 1
for clause in subgoal[0]:
	print clause
#print solver.dimacs()

# #print solver.sexpr()
# print >>sys.stderr, "Running solver..."
# z3.set_param(verbose=10)
# print solver.check()
# print solver.model()
