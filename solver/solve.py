#!/usr/bin/python
import sudoku
import optparse

parser = optparse.OptionParser()
parser.add_option( "-p", "--puzzle-file", default=None, dest="puzzle_file" )
(options, args) = parser.parse_args()

lines = open(options.puzzle_file,"r").readlines()
lines = [l.strip() for l in lines if l != ""]

s2 = sudoku.Sudoku( size=len(lines) )

def cell(c):
    if c == '*':
        return 0
    else:
        return int(c)

for i in range(len(lines)):
    s2.fix_row( i, [cell(c) for c in lines[i]] )

s2.shuffle()

s2.solve().print_board()

print "Original:"
s2.print_board()
