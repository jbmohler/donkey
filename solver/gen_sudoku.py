#!/usr/bin/python
import sudoku
import optparse
import random

parser = optparse.OptionParser()
parser.add_option( "-s", "--size", default=9, dest="size" )
parser.add_option( "-f", "--fixed", default=5, dest="fixed" )
(options, args) = parser.parse_args()

s = sudoku.Sudoku( size = options.size )
s.shuffle()
soln = s.solve()

to_print = sudoku.Sudoku( size = options.size )
for i in random.sample( range(s.size() ** 2), int(options.fixed) ):
	to_print.fix_point( i, soln.choice( i ) )

to_print.csv_board( False )
print "The Solution:"
soln.csv_board( False )
