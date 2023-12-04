"""
Advent of Code 2023

`Day 2 <https://adventofcode.com/2023/day/2>`_:
Cube Conundrum
"""
import enum
import functools
import operator
import os
import re
import sys


RE_GAME = re.compile(r"Game (\d+): (.*)")
RE_DRAW = re.compile(r"(\d+) (red|green|blue)")


class RgbIndex(enum.IntEnum):
    """ Enum for mapping color word to RGB index. """
    red = 0
    green = 1
    blue = 2


def parse_game(value):
    raw_gameno, rest = RE_GAME.match(value).groups()
    gameno = int(raw_gameno)
    game = []
    for raw_rgb in rest.split(";"):
        rgb = [0, 0, 0]
        for count, color in RE_DRAW.findall(raw_rgb):
            rgb[RgbIndex[color]] = int(count)
        game.append(tuple(rgb))
    return gameno, game


def read_games(fd):
    """ Read calorie counts from file-like. """
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            yield parse_game(line)
        except Exception as e:
            raise ValueError("Invalid game on line %d: %s (%s)"
                             % (lineno, repr(line), e))


MAX_RGB = (12, 13, 14)


def is_possible(game):
    """ Check if a list of game are possible """
    for rgb in game:
        if any(count > limit for count, limit in zip(rgb, MAX_RGB)):
            return False
    return True


def solve_pt1(games):
    """ Sum of possible game numbers. """
    return sum(gameno for gameno, game in games if is_possible(game))


def get_game_min(game):
    """ Get the minimum number of cubes in a game. """
    min_rgb = [0, 0, 0]
    for rgb in game:
        min_rgb = [max(a, b) for a, b in zip(min_rgb, rgb)]
    return tuple(min_rgb)


def get_rgb_power(rgb):
    """ Get the *power* of a set of cubes. """
    return functools.reduce(operator.mul, rgb, 1)


def solve_pt2(games):
    """ Sum of cube *power* of the minimum cube set from all games. """
    return sum(get_rgb_power(get_game_min(game)) for _, game in games)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            games = list(read_games(f))

        pt1 = solve_pt1(games)
        print('Part 1:', pt1)

        pt2 = solve_pt2(games)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
