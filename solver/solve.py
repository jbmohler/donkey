#!/usr/bin/python
import sudoku2
import optparse

parser = optparse.OptionParser()
parser.add_option( "-p", "--puzzle-file", default=None, dest="puzzle_file" )
(options, args) = parser.parse_args()

s2 = sudoku2.Sudoku_FromFile( options.puzzle_file )
s2.shuffle()
print s2.solve()
print "Original:"
print s2
