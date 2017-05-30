import numpy

ORD_A = ord('a')

def to_move(pos):
	return chr(ORD_A + pos[1]) + str(pos[0] + 1)

def to_pos(move):
	return int(move[1:]) - 1, ord(move[0]) - ORD_A

def list_positions(board, player):
    return numpy.vstack(numpy.nonzero(board == player)).T

