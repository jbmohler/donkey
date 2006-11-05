#!/usr/bin/python
import string
import copy
import getopt
import random

class Impossible:
	pass

class Sudoku:
	def __init__( self, small_size = None, size = None ):
		assert( small_size is None or size is None )
		if small_size is None:
			self.small_size = int(math.sqrt(size))
		else:
			self.small_size = small_size

		self.board = [[range(1,self.size() + 1) for j in range(self.size())] for k in range(self.size())]

	def size( self ):
		return self.small_size ** 2

	def print_board( self ):
		for r in self.board:
			for cell in r:
				s = ''
				if type(cell) is list:
					s = ''.join( map( lambda x: str(x), cell ) )
				else:
					s = str( cell )
				print '%-*s' % (self.size()+1, s),
			print '\n',

	def shuffle( self ):
		s = self.size()
		for i in range(s):
			for j in range(s):
				if type(self.board[i][j]) is list:
					random.shuffle( self.board[i][j] )

	def fix_grid( self, content ):
		assert( type(content) is list )
		assert( len(content) == self.size() )

		for i in range( self.size() ):
			if content[i] != None:
				assert( type(content[i]) is list )
				self.fix_row( i, content[i] )

	def fix_row( self, row, content ):
		assert( type(content) is list )
		assert( len(content) == self.size() )

		for i in range( self.size() ):
			if content[i] != 0 and content[i] != None:
				self.fix_point( row, i, content[i] )

	def fix_point( self, x, y, n ):
		if not type(self.board[x][y]) is list:
			if n != self.board[x][y]:
				raise Impossible

		self.board[x][y] = n

		for i in range(self.size()):
			if x != i:
				self.remove_choice( i, y, n )
			if y != i:
				self.remove_choice( x, i, n )

		offset_x = x/self.small_size
		offset_y = y/self.small_size
		for i in range(self.small_size):
			for j in range(self.small_size):
				this_x = i + offset_x * self.small_size
				this_y = j + offset_y * self.small_size
				if this_x != x and this_y != y:
					self.remove_choice( this_x, this_y, n )

	def remove_choice( self, x, y, n ):
		if (type(self.board[x][y]) is list) and (n in self.board[x][y]):
			self.board[x][y].remove( n )
			if len(self.board[x][y]) == 1:
				self.fix_point( x, y, self.board[x][y][0] )
		elif (not type(self.board[x][y]) is list) and n == self.board[x][y]:
			raise Impossible

	def successful( self ):
		print "Success!"
		self.print_board()

	def next_index_min_list( self, current ):
		min_list_size = self.size()
		min_cell = False
		for i in range( self.size() ):
			for j in range( self.size() ):
				if type(self.board[i][j]) is list:
					if len(self.board[i][j]) < min_list_size:
						min_list_size = len(self.board[i][j])
						min_cell = i * self.size() + j

		return min_cell

	def solve( self, index ):
	#	depth = depth + 1
		x = index / self.size()
		y = index % self.size()

		if type(self.board[x][y]) is list:
			if len(self.board[x][y]) > 0:
				for n in self.board[x][y]:
					next = copy.deepcopy( self )
					try:
						next.fix_point( x, y, n )
					except Impossible:
						continue
					next_up = next.next_index_min_list( index )
					if not next_up:
						next.successful()
						return True
					if next.solve( next_up ):
						return True
			else:
				print "Thwarted:"
				self.print_board()
				return False
		else:
			next_up = self.next_index_min_list( index )
			if not next_up:
				self.successful()
				return True
			if self.solve( next_up ):
				return True
