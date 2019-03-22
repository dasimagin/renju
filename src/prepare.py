import yt.wrapper as yt

from itertools import permutations

names = ['dummy-1', 'dummy-2']

def generate_games(table, names, game_n):
    return game_n * [{'black': black, 'white': white} for black, white in permutations(names, 2)]

def main():
    game_table = '//home/maps_mrc/dasimagin/games'

    games = game_n * [{'black': black, 'white': white} for black, white in permutations(names, 2)]
    yt.write_table(game_table, games)


if __name__ == "__main__":
    main()
