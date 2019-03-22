# -*- coding: utf-8 -*-

import json
import logging
import sys

from agent import BackendAgent
from renju import Player, run

name_to_cmd = {
    'dummy-1': 'python3 dummy.py',
    'dummy-2': 'python3 dummy.py',
}

def push(row):
    print(json.dumps(row))

def make(name):
    return BackendAgent(name_to_cmd[name], name)

def main():
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s', level=logging.INFO)

    for line in sys.stdin:
        row = json.loads(line)
        black, white = row['black'], row['white']

        result = run(make(black), make(white), max_move_n=60, timeout=3)

        if result == Player.BLACK:
            push({'name': black, 'score': 3})
            push({'name': white, 'score': 0})
        elif result == Player.WHITE:
            push({'name': black, 'score': 0})
            push({'name': white, 'score': 3})
        else:
            push({'name': black, 'score': 1})
            push({'name': white, 'score': 1})


if __name__ == "__main__":
    main()
