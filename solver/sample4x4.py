#!/usr/bin/python
import sudoku

s = sudoku.Sudoku( small_size = 2 )
s.shuffle()
s.print_board()
s.solve( 0 )
