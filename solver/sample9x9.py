#!/usr/bin/python
import sudoku

s2 = sudoku.Sudoku( small_size = 3 )

#s2.fix_point( 1, 1, 1 )
#s2.fix_point( 8, 2, 3 )
#s2.fix_point( 4, 4, 8 )
#s2.fix_point( 5, 5, 5 )

s2.fix_row( 0, [0,1,0,0,0,0,0,0,0] )
s2.fix_row( 1, [0,0,0,0,0,0,0,6,0] )
s2.fix_row( 2, [6,0,0,0,8,1,0,0,4] )
s2.fix_row( 3, [0,6,0,0,0,7,5,0,0] )
s2.fix_row( 4, [0,0,0,1,6,0,0,0,0] )
s2.fix_row( 5, [8,0,0,0,0,0,0,0,2] )
s2.fix_row( 6, [0,4,9,0,0,5,0,0,0] )
s2.fix_row( 7, [0,0,0,0,0,9,7,0,0] )
s2.fix_row( 8, [0,0,7,0,0,0,0,1,0] )

s2.shuffle()

s2.solve().print_board()

print "Original:"
s2.print_board()
