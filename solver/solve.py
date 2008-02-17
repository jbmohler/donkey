#!/usr/bin/python
import sudoku
import optparse

parser = optparse.OptionParser()
parser.add_option( "-p", "--puzzle-file", default=None, dest="puzzle_file" )
(options, args) = parser.parse_args()

s2 = sudoku.Sudoku_FromFile( options.puzzle_file )
s2.shuffle()
s2.solve().print_board()
print "Original:"
s2.print_board()
