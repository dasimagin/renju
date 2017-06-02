import logging
import random

import backend
import renju
import util


def choose_random_move(board):
    positions = util.list_positions(board, renju.Player.NONE)
    return util.to_move(random.choice(positions))

def main():
    logging.basicConfig(filename='dummy.log', level=logging.DEBUG)
    logging.debug("Start dummy backend...")

    try:
        while True:
            logging.debug("Wait for game update...")
            game = backend.wait_for_game_update()
            logging.debug('Board:\n' + str(game.board()))

            move = choose_random_move(game.board())
            backend.move(move)
            logging.debug('make move: ' + move)
    except:
        logging.error('Error!', exc_info=True, stack_info=True)


if __name__ == "__main__":
    main()
