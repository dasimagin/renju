import renju
import sys

def wait_for_game_update():
    if not sys.stdin.closed:
        game_dumps = sys.stdin.readline()

        if game_dumps:
            return renju.Game.loads(game_dumps)

    return None

def set_move(move):
    if sys.stdout.closed:
        return False

    sys.stdout.write(move + '\n')
    sys.stdout.flush()

    return True
