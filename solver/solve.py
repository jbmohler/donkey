#!/usr/bin/python
import sudoku
import optparse

parser = optparse.OptionParser()
parser.add_option( "-p", "--puzzle-file", default=None, dest="puzzle_file" )
(options, args) = parser.parse_args()

lines = open(options.puzzle_file,"r").readlines()
lines = [l.strip() for l in lines if l != ""]

s2 = sudoku.Sudoku( size=len(lines) )

#s2.fix_point( 1, 1, 1 )
#s2.fix_point( 8, 2, 3 )
#s2.fix_point( 4, 4, 8 )
#s2.fix_point( 5, 5, 5 )

def cell(c):
    if c == '*':
        return 0
    else:
        return int(c)

for i in range(len(lines)):
    s2.fix_row( i, [cell(c) for c in lines[i]] )
#s2.fix_row( 1, [0,0,0,0,0,0,0,6,0] )
#s2.fix_row( 2, [6,0,0,0,8,1,0,0,4] )
#s2.fix_row( 3, [0,6,0,0,0,7,5,0,0] )
#s2.fix_row( 4, [0,0,0,1,6,0,0,0,0] )
#s2.fix_row( 5, [8,0,0,0,0,0,0,0,2] )
#s2.fix_row( 6, [0,4,9,0,0,5,0,0,0] )
#s2.fix_row( 7, [0,0,0,0,0,9,7,0,0] )
#s2.fix_row( 8, [0,0,7,0,0,0,0,1,0] )

s2.shuffle()

s2.solve().print_board()

print "Original:"
s2.print_board()
