Readme.txt
==========

Author:			Greg Egan
Date:			24 February 2019
Version 1.1:	25 February 2019, describes new "nsk" option that implements Robin Houston's non-standard kernels

Building and testing
--------------------

This file describes the program PermutationChains.c, which searches for short superpermutations.  The algorithm it uses
is based on the approach described by Bogdan Coanda here:

	https://groups.google.com/d/msg/superpermutators/KNhmzQy99ic/obl6pCt5HwAJ

but any errors are entirely my own.

PermutationChains.c is a single, standalone file for a command-line C program, which should compile, link and run in
any command-line environment.

Usage is:

	PermutationChains n [options ...]

where n specifies the number of digits the permutations use.  Where the program succeeds, it produces permutations of
length:

	n! + (n–1)! + (n–2)! + (n–3)! + n – 4

e.g. for n=5 of length 153, for n=6 of length 872, and for n=7 of length 5907.

After building the program, to check that it is working you could try:

	PermutationChains 5

which should find 6 solutions more or less instantly, or:

	PermutationChains 6 ffc

which should find 36 solutions, again almost instantly, or:

	PermutationChains 6

which should find 42,288 solutions in a time of the order of 1 minute.

At the time of writing, the only search for n=7 solutions that is known to complete in a reasonable time is:

	PermutationChains 7 fullSymm limStab ffc
	
which should find 762 solutions in roughly half an hour.

(These benchmarks are for an iMac with a 4.2 GHz Intel Core i7 processor.)


Options
-------

The following options can be given on the command line.

Options that control what is shown on the console (default is just to count each solution as it's found):

	verbose								Give lots of details of initial setup
	showSols							Show details of each solution as it's found
	trackPartial						Show each new largest partial solution

Options for the choice of kernel (default is the first 3-cycle):

	ffc									Use the first 4-cycle as the kernel
	nsk<specifier>						Use a non-standard kernel.  The details are discussed below.

Options for the choice of anchor points on the kernel (default is to allow trees anchored anywhere on the kernel):

	lastAnchor							Only anchor at the last 2-cycle (or for symmPairs, also its pair)
	fixedPointAnchor					With lastAnchor, allow trees anchored at points that are their own pair

Options for the choice of orbit type:

	stabiliser							Use the full stabiliser group of the kernel
	limStab								Use the stabiliser of a subset of the kernel
	symmPairs							Use a 2-fold symmetry that preserves the kernel
	littleGroup							Use a subgroup of the stabiliser of order n-2
	blocks								Use cyclic blocks of size n-2 (not orbits of any symmetry)

Options for how to handle orbits:

	fixedPoints							Include fixed points of symmPairs
	fullSymm							Require the solution to consist entirely of orbits

Options to filter solutions:

	treesOnly							Filter solutions to only output strict trees in the 2-cycle graph
	
Options for the structure of solutions:

	coverFirst							Attempt to cover the 1-cycles not in the kernel with disjoint 2-cycles first.
										For non-standard kernels that include partial 2-cycles, the whole of the
										2-cycle is excluded from the set to be covered.
	
Non-standard kernels
--------------------

A non-standard kernel is specified by a list of the numbers of complete 1-cycles, separated by weight-2
edges, before using either a weight-3 edge (if the next digit follows directly after), or a weight-4 edge
(if a space or a dash separates the digits; if you want to use a space, you will need to enclose the whole option
in quotation marks.)

For example:

	SuperPermutations 6 nsk5555-555355
	
uses a kernel with four complete 2-cycles (each with 5 1-cycles separated by weight-2 edges), then a weight-4
edge to a section with three complete 2-cycles, then 3 consecutive 1-cycles, then a weight-3 edge to two complete
2-cycles.

Non-standard kernels will generally lack the kind of symmetries of the standard kernels. However, if you supply
a palindromic non-standard kernel, you can use the "symmPairs" symmetry option, which will apply the symmetry
that maps the kernel back into itself in reversed order.
	
Specifics of symmetry options
-----------------------------

symmPairs
---------

The 2-fold symmetry used by the "symmPairs" option is defined somewhat arbitrarily for different choice of n and kernel.

* n=5, 3-cycle kernel

Apply the cycle (1 3) to the permutations and reverse.  This exchanges two of the 2-cycles in the kernel and leaves one
fixed.  Choosing the options "symmPairs fullSymm" for n=5 will reduce the solution set from the usual 6 to just 2, which
are both invariant under this symmetry.

* n=7, 3-cycle kernel

Apply the cycles (1 2)(3 5) to the permutations and reverse.  This exchanges two pairs of 2-cycles in the kernel and leaves one fixed.

* n=7, 4-cycle kernel

Apply the cycle (1 3) to the permutations and reverse.

* Palindromic non-standard kernels

Apply the symmetry that maps the kernel back into itself in reversed order.

limStab
-------

The option "limStab" is only defined for:

* n=7, 4-cycle kernel

The orbits are obtained from the stabiliser of the 1st, 6th, 15th and 20th 2-cycles in the kernel.  This is a group of order 4,
generated by:

(1 3) and reverse
(2 4)(5 6) and reverse

littleGroup
-----------

This only applies to the 3-cycle kernel.

For odd n, this uses a group of order n-2 generated by the cycle (1 2 3 ... n-2).

For even n, for n=6 the group used was found empirically to have orbits that encompassed all but one element of a small
number of solutions.  This group is generated by:

(1 3) and reverse
(2 4) and reverse.

For n=8, an analogous group of order 6 is included in the program, but the usefulness of it is entirely unknown at this point.


Files written
-------------

Each search produces two results file, one containing the superpermutations (one per line), and the other
containing a list of 2-cycles on which the solution is based, as n-tuples of digits, grouped into lists with
curly braces {}.  These files have names of the form:

	<n>_<len>(_options).txt
	<n>_<len>_twoCycles(_options).txt

where len is the length of the superpermutations, and _options reflects the options chosen, so that different
choices give different files rather than overwriting existing files.

(These files are closed after each new solution is added, so the program can be terminated in the middle of
a search without losing any results that have been found.)

In addition to these output files, the program writes, and reads back, a file of the form:

	IntersectionFlags<n>.dat
	
which contains data on the intersections between 2-cycles.  This saves it from being recalculated on
repeated runs with the same n.

