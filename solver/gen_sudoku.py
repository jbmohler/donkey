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
for i in random.sample( range(s.size() ** 2), int(options.fixed) ):
	if type(s.choice( i )) is list:
		s.fix_point( i, s.choice( i )[0] )
if s.solve( 0 ):
	s.csv_board( False )
	
