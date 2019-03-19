import concurrent.futures
import enum
import itertools
import logging
import numpy
import sys
import time
import traceback


POS_TO_LETTER = 'abcdefghjklmnop'
LETTER_TO_POS = {letter: pos for pos, letter in enumerate(POS_TO_LETTER)}

def to_move(pos):
    return POS_TO_LETTER[pos[1]] + str(pos[0] + 1)

def to_pos(move):
    return int(move[1:]) - 1, LETTER_TO_POS[move[0]]

def list_positions(board, player):
    return numpy.vstack(numpy.nonzero(board == player)).T

def sequence_length(board, I, J, value):
    length = 0

    for i, j in zip(I, J):
        if board[i, j] != value:
            break
        length += 1

    return length


def check_horizontal(board, pos):
    player = board[pos]
    if not player:
        return False

    i, j = pos
    length = 1

    length += sequence_length(
        board,
        itertools.repeat(i),
        range(j + 1, min(j + Game.line_length, Game.width)),
        player
    )

    length += sequence_length(
        board,
        itertools.repeat(i),
        range(j - 1, max(j - Game.line_length, -1), -1),
        player
    )

    return length >= Game.line_length

def check_vertical(board, pos):
    player = board[pos]
    if not player:
        return False

    i, j = pos
    length = 1

    length += sequence_length(
        board,
        range(i + 1, min(i + Game.line_length, Game.height)),
        itertools.repeat(j),
        player
    )

    length += sequence_length(
        board,
        range(i - 1, max(i - Game.line_length, -1), -1),
        itertools.repeat(j),
        player
    )

    return length >= Game.line_length

def check_main_diagonal(board, pos):
    player = board[pos]
    if not player:
        return False

    i, j = pos
    length = 1

    length += sequence_length(
        board,
        range(i + 1, min(i + Game.line_length, Game.height)),
        range(j + 1, min(j + Game.line_length, Game.width)),
        player
    )

    length += sequence_length(
        board,
        range(i - 1, max(i - Game.line_length, -1), -1),
        range(j - 1, max(j - Game.line_length, -1), -1),
        player
    )

    return length >= Game.line_length

def check_side_diagonal(board, pos):
    player = board[pos]
    if not player:
        return False

    i, j = pos
    length = 1

    length += sequence_length(
        board,
        range(i - 1, max(i - Game.line_length, -1), -1),
        range(j + 1, min(j + Game.line_length, Game.width)),
        player
    )

    length += sequence_length(
        board,
        range(i + 1, min(i + Game.line_length, Game.height)),
        range(j - 1, max(j - Game.line_length, -1), -1),
        player
    )

    return length >= Game.line_length

def check(board, pos):
    if not board[pos]:
        return False

    return check_vertical(board, pos) \
        or check_horizontal(board, pos) \
        or check_main_diagonal(board, pos) \
        or check_side_diagonal(board, pos)


class Player(enum.IntEnum):
    NONE = 0
    BLACK = -1
    WHITE = 1

    def another(self):
        return Player(-self)

    def __repr__(self):
        if self == Player.BLACK:
            return 'black'
        elif self == Player.WHITE:
            return 'white'
        else:
            return 'none'

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def from_str(s):
        if s == 'black':
            return Player.BLACK
        elif s == 'white':
            return Player.WHITE
        else:
            return Player.NONE


class Game:
    width, height = 15, 15
    shape = (width, height)
    line_length = 5

    def __init__(self):
        self._result = Player.NONE
        self._player = Player.BLACK
        self._board = numpy.full(self.shape, Player.NONE, dtype=numpy.int8)
        self._positions = list()

    def __bool__(self):
        return self.result() == Player.NONE and \
            len(self._positions) < self.width * self.height

    def move_n(self):
        return len(self._positions)

    def player(self):
        return self._player

    def result(self):
        return self._result

    def board(self):
        return self._board

    def positions(self, player=Player.NONE):
        if not player:
            return self._positions

        begin = 0 if player == Player.BLACK else 1
        return self._positions[begin::2]

    def dumps(self):
        return ' '.join(map(to_move, self._positions))

    @staticmethod
    def loads(dump):
        game = Game()
        for pos in map(to_pos, dump.split()):
            game.move(pos)
        return game


    def is_posible_move(self, pos):
        return 0 <= pos[0] < self.height \
            and 0 <= pos[1] < self.width \
            and not self._board[pos]

    def move(self, pos):
        assert self.is_posible_move(pos), 'impossible pos: {pos}'.format(pos=pos)

        self._positions.append(pos)
        self._board[pos] = self._player

        if not self._result and check(self._board, pos):
            self._result = self._player
            return

        self._player = self._player.another()

def number_shift(n):
    if n >= 100:
        return (0.32, 0.15)
    if n >= 10:
        return (0.22, 0.15)
    return (0.10, 0.15)

class PyPlotUI:
    def __init__(self, black='black', white='white'):
        matplotlib.pyplot.ion()
        self._board = matplotlib.pyplot.figure(figsize=(8, 8))

        self._ax = self._board.add_subplot(111)
        self._ax.set_navigate(False)

        self._ax.set_title('{black} vs {white}'.format(black=black, white=white))

        self._ax.set_xlim(-1, Game.width)
        self._ax.set_ylim(-1, Game.height)

        self._ax.set_xticks(numpy.arange(0, Game.width))
        self._ax.set_xticklabels(POS_TO_LETTER)

        self._ax.set_yticks(numpy.arange(0, Game.height))
        self._ax.set_yticklabels(numpy.arange(1, Game.height + 1))

        self._ax.grid(zorder=2)

        self._black= self._ax.scatter(
            (),(),
            color = 'black',
            s = 500,
            edgecolors = 'black',
            zorder = 3
        )
        self._white = self._ax.scatter(
            (),(),
            color = 'white',
            s = 500,
            edgecolors = 'black',
            zorder = 3
        )

        self._probs = self._ax.imshow(
            numpy.zeros(Game.shape),
            cmap = 'Reds',
            interpolation = 'none',
            vmin = 0.0,
            vmax = 1.0,
            zorder = 1
        )

        self._board.show()


    def update(self, game, probs):
        board = game.board()

        black_positions = list_positions(board, Player.BLACK)
        self._black.set_offsets(black_positions[:, (1, 0)])

        white_positions = list_positions(board, Player.WHITE)
        self._white.set_offsets(white_positions[:, (1, 0)])

        self._ax.texts = []
        for n, (i, j) in enumerate(game.positions(), 1):
            shift = number_shift(n)
            self._ax.text(
                j - shift[0],
                i - shift[1],
                str(n),
                color = 'white' if n % 2 else 'black',
                fontsize = 10,
                zorder = 4
            )

        self._probs.set_data(probs / max(probs.max(), 1e-6))

        self._board.canvas.draw()

        return self

MAX_MOVE_N = Game.width * Game.height

def loop(game, black, white, max_move_n=MAX_MOVE_N , timeout=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        for agent in itertools.cycle([black, white]):
            if not game or game.move_n() >= max_move_n:
                break

            future = executor.submit(lambda game: agent.move(game), game)
            pos = to_pos(future.result(timeout=timeout))
            game.move(pos)

            yield game


def run(black, white, max_move_n=60, timeout=3):
    game = Game()

    try:
        for game in loop(game, black, white, max_move_n=max_move_n, timeout=timeout):
            # logging.debug(game.dumps())
            pass


    except:
        logging.error('Error!', exc_info=True, stack_info=True)
        return game.player().another(), game.dumps()

    return game.result(), game.dumps()
