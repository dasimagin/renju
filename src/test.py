#!/usr/local/bin/python3

import collections
import itertools
import logging
import time

from renju import run, Player
from agent import BackendAgent


def game(max_move_n=60, timeout=3, timeinit=5):
    white = BackendAgent('python3 dummy.py', 'White')
    black = BackendAgent('python3 dummy.py', 'Black')

    logging.debug('%s vs %s', black.name(), white.name())

    logging.debug('Load backends...')
    time.sleep(timeinit)
    logging.debug('Start game!')

    result, moves = run(black, white, max_move_n=max_move_n, timeout=timeout)
    logging.debug('result: %s', result)
    logging.debug('moves: %s', moves)


def main():
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s', level=logging.DEBUG)
    game()

if __name__ == "__main__":
    main()
