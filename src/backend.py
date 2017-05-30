import renju
import sys

def wait_for_game_update():
	data = sys.stdin.buffer.readline().rstrip()
	return renju.Game.loads(data.decode())

def move(move):
    sys.stdout.buffer.write(move.encode() + b'\n')
    sys.stdout.flush()
