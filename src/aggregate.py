# -*- coding: utf-8 -*-

import json
import sys
import collections

def push(row):
    print(json.dumps(row))

def main():
    scores = collections.defaultdict(int)

    for row in map(json.loads, sys.stdin):
        scores[row['name']] += row['score']

    for name, score in scores.items():
        push({'name': name, 'score': score})


if __name__ == "__main__":
    main()
