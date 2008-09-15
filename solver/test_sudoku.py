#!/usr/bin/python

import resource
def cputime(t=0):
    try:
        t = float(t)
    except TypeError:
        t = 0.0
    u,s = resource.getrusage(resource.RUSAGE_SELF)[:2]
    return u+s - t


games=[
#	"near_worst_case.txt",
	"qassim_hamza.txt",
	"sample_01.txt",
	"top_1465_77.txt"]

import gc
gc.disable()

for g in games:
	print "Game:  %s" % (g,)
	from sudoku1 import *
	s=Sudoku_FromFile(g)
	t1=cputime()
	for i in range(10):
		s.shuffle()
		s.solve()
	t2=cputime()
	print "Sudoku v. 1:  %.3f" % (t2-t1)
	gc.collect()
	
	from sudoku2 import *
	s=Sudoku_FromFile(g)
	t1=cputime()
	for i in range(10):
		s.shuffle()
		s.solve()
	t2=cputime()
	print "Sudoku v. 2:  %.3f" % (t2-t1)
	gc.collect()

	from sudoku3 import *
	s=Sudoku_FromFile(g)
	t1=cputime()
	for i in range(10):
		s.shuffle()
		s.solve()
	t2=cputime()
	print "Sudoku v. 3:  %.3f" % (t2-t1)
	gc.collect()
