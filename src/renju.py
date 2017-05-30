import concurrent
import enum
import itertools
import matplotlib
import numpy
import string
import sys
import time
import traceback
import util


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


class Game:
    width, height = 15, 15
    shape = (width, height)

    def __init__(self):
        self._result = Player.NONE
        self._player = Player.BLACK
        self._board = numpy.full(self.shape, Player.NONE, dtype=numpy.int8)
        self._positions = list()

    def __bool__(self):
        return self.result() == Player.NONE \
            and len(self._positions) < self.width * self.height

    def dumps(self):
        return ' '.join(map(util.to_move, self._positions))

    @staticmethod
    def loads(dump):
        game = Game()
        for pos in map(util.to_pos, dump.split()):
            game.move(pos)
        return game

    def result(self):
        return self._result

    def player(self):
        return self._player

    def board(self):
        return self._board.copy()

    def positions(self):
        return self._positions.copy()

    def is_posible_move(self, pos):
        return 0 <= pos[0] < self.height \
            and 0 <= pos[1] < self.width \
            and not self._board[pos]

    def move(self, pos):
        assert self.is_posible_move(pos), 'impossible pos: {pos}'.format(pos=pos)

        self._positions.append(pos)
        self._board[pos] = self._player
        self._player = self._player.another()

def number_shift(n):
    if n >= 100:
        return (0.35, 0.15)
    if n >= 10:
        return (0.25, 0.15)
    return (0.12, 0.15)

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
        self._ax.set_xticklabels(string.ascii_lowercase[:Game.width])

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


    def update(self, game, probs=numpy.zeros(Game.shape)):
        board = game.board()

        black_positions = util.list_positions(board, Player.BLACK)
        self._black.set_offsets(black_positions[:, (1, 0)])

        white_positions = util.list_positions(board, Player.WHITE)
        self._white.set_offsets(white_positions[:, (1, 0)])

        colors = ['black', 'white']
        self._ax.texts = []
        for n, (i, j) in enumerate(game.positions(), 1):
            shift = number_shift(n)
            self._ax.text(

                j - shift[0],
                i - shift[1],
                str(n),
                color = colors[n % 2],
                fontsize = 11,
                zorder = 4
            )

        self._probs.set_data(probs / 2 * max(probs.max(), 1e-9))

        self._board.canvas.draw()

        return self

def loop(game, black, white, timeout=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        yield game, numpy.zeros(game.shape)

        for agent in itertools.cycle([black, white]):
            if not game:
                break

            future = executor.submit(lambda game: agent.policy(game), game)
            probs = future.result(timeout=timeout)

            pos = numpy.unravel_index(probs.argmax(), game.shape)
            game.move(pos)

            yield game, probs

def run_test(black, white, timeout=None):
    game = Game()
    ui = PyPlotUI(black.name(), white.name())

    try:
        for game, probs in loop(game, black, white, timeout):
            ui.update(game, probs)
            time.sleep(1.0) # test pause

    except:
        _, e, tb = sys.exc_info()
        print(e)
        traceback.print_tb(tb)
        return game.player().another()

    return game.result()
