import logging
import os
import random

import backend
import renju


def choose_random_move(board):
    positions = renju.list_positions(board, renju.Player.NONE)
    return renju.to_move(random.choice(positions))

LOG_FORMAT = '%(levelname)s:%(asctime)s: dummy-{0}: %(message)s'.format(os.getpid())

def main():
    pid = os.getpid()
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
    logging.debug("Start dummy backend...")

    try:
        while True:
            logging.debug("Wait for game update...")
            game = backend.wait_for_game_update()

            if not game:
                logging.debug("Game is over!")
                return

            logging.debug('Game: %s', game.dumps())
            move = choose_random_move(game.board())

            if not backend.set_move(move):
                logging.error("Impossible set move!")
                return

            logging.debug('Random move: %s', move)
    except:
        logging.error('Error!', exc_info=True, stack_info=True)


if __name__ == "__main__":
    main()
