#!/usr/bin/python
import string
import copy

small_size = 3 # sqrt of size of board
size = small_size ** 2

board = []

for i in range(size):
	board.append( [] )
	for j in range(size):
		board[i].append( range(1,size+1) )

def print_board( board ):
	for r in board:
		for cell in r:
			s = ''
			if type(cell) is list:
				s = ''.join( map( lambda x: str(x), cell ) )
			else:
				s = str( cell )
			print '%-*s' % (size+1, s),
		print '\n',

def fix_grid( content, board ):
	assert( type(content) is list )
	assert( len(content) == size )

	for i in range( size ):
		if content[i] != None:
			assert( type(content[i]) is list )
			fix_row( i, content[i], board )

def fix_row( row, content, board ):
	assert( type(content) is list )
	assert( len(content) == size )

	for i in range( size ):
		if content[i] != 0 and content[i] != None:
			if not fix_point( row, i, content[i], board ):
				return False

	return True

def fix_point( x, y, n, board ):
	if not type(board[x][y]) is list:
		return False

	board[x][y] = n

	for i in range(size):
		if x != i and (type(board[i][y]) is list) and (n in board[i][y]):
			board[i][y].remove( n )
		if y != i and (type(board[x][i]) is list) and (n in board[x][i]):
			board[x][i].remove( n )

	offset_x = x/3
	offset_y = y/3
	for i in range(small_size):
		for j in range(small_size):
			this_x = i + offset_x * 3
			this_y = j + offset_y * 3
			if this_x != x and this_y != y and (type(board[this_x][this_y]) is list) and (n in board[this_x][this_y]):
				board[this_x][this_y].remove( n )

	return True

def successful( board ):
	print "Success!"
	print_board( board )

def next_index_increment( current, board ):
	if current == size ** 2 - 1:
		return False
	else:
		return current + 1

def next_index_min_list( current, board ):
	min_list_size = size
	min_cell = False
	for i in range( size ):
		for j in range( size ):
			if type(board[i][j]) is list:
				if len(board[i][j]) < min_list_size:
					min_list_size = len(board[i][j])
					min_cell = i * size + j

	return min_cell

def solve( index, board, next_func ):
	x = index / size
	y = index % size

	if type(board[x][y]) is list:
		if len(board[x][y]) > 0:
			for n in board[x][y]:
				next = copy.deepcopy( board )
				fix_point( x, y, n, next )
				next_up = next_func( index, board )
				if not next_up:
					successful( board )
					return True
				if solve( next_up, next, next_func ):
					return True
		else:
			print "Thwarted:"
			print_board( board )
			return False
	else:
		next_up = next_func( index, board )
		if not next_up:
			successful( board )
			return True
		if solve( next_up, board, next_func ):
			return True

fix_point( 1, 1, 1, board )
fix_point( 8, 2, 3, board )
fix_point( 4, 4, 8, board )
fix_point( 5, 5, 5, board )

#fix_row( 0, (0,3,0,0,0,1,0,0,0), board )
#fix_row( 1, (0,0,6,0,0,0,0,5,0), board )
#fix_row( 2, (5,0,0,0,0,0,9,8,3), board )
#fix_row( 3, (0,8,0,0,0,6,3,0,2), board )
#fix_row( 4, (0,0,0,0,5,0,0,0,0), board )
#fix_row( 5, (9,0,3,8,0,0,0,6,0), board )
#fix_row( 6, (7,1,4,0,0,0,0,0,9), board )
#fix_row( 7, (0,2,0,0,0,0,8,0,0), board )
#fix_row( 8, (0,0,0,4,0,0,0,3,0), board )

solve( 0, board, next_index_min_list )

print "Original:"
print_board( board )
