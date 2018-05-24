#!/usr/local/bin/python3

import collections
import itertools
import logging
import time

from renju import run, Player
from agent import BackendAgent


agents = ['dummy', 'dummy']


# white = BackendAgent('python3 dummy.py', 'dummy')
# black = BackendAgent('python3 dummy.py', 'dummy')


def game(black, white, max_move_n=60, timeout=3, timeinit=15):
    black = BackendAgent('dist/dummy', 'dummy')
    white = BackendAgent('dist/dummy', 'dummy')

    # black = BackendAgent('python3 dummy.py', 'dummy')
    # white = BackendAgent('python3 dummy.py', 'dummy')


    logging.debug('%s vs %s', black.name(), white.name())

    logging.debug('Load backends...')
    time.sleep(timeinit)
    logging.debug('Start game!')

    result, moves = run(black, white, max_move_n=60, timeout=10)
    logging.debug('result: %s', result)
    logging.debug('moves: %s', moves)


def main():
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s', level=logging.DEBUG)
    game(None, None)

if __name__ == "__main__":
    main()
