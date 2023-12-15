"""
Advent of Code 2023

`Day 11 <https://adventofcode.com/2023/day/11>`_:
Cosmic Expansion
"""
import functools
import itertools
import os
import sys


def read_matrix(fd):
    """ Read position and value from file-like *fd*. """
    rownum = 0
    for lineno, line in enumerate(fd, 1):
        if not line.strip():
            continue
        try:
            row = tuple(line.strip())
            for colnum, char in enumerate(row):
                yield (rownum, colnum), char
            rownum += 1
        except Exception as e:
            raise ValueError('invalid input on line %d (%r): %s' %
                             (lineno, line, e))


def get_galaxies(matrix):
    """" Extract galaxy positions from input matrix. """
    return set(p for p in matrix if matrix[p] == "#")


def expand(galaxies, factor=2):
    """"
    Expand space between galaxies.

    :param set galaxies: A set of (row, col) coordinates for each galaxy
    :param int factor: How many spaces each empty space should expand to

    :returns set: A set of new (row, col) coordinates for each input galaxy.
    """
    # expand rows, then columns
    for idx in (0, 1):
        prev = offset = 0
        galaxies, to_expand = set(), galaxies
        for galaxy in sorted(to_expand, key=lambda t: t[idx]):
            if galaxy[idx] > prev + 1:
                offset += (galaxy[idx] - prev - 1) * (factor - 1)
            prev = galaxy[idx]
            galaxies.add((
                galaxy[0] + (offset if idx == 0 else 0),
                galaxy[1] + (offset if idx == 1 else 0),
            ))

    return galaxies


def distance(position, origin=(0, 0)):
    """ Get the *manhattan distance* between two points. """
    x, y = origin
    dx, dy = position
    return abs(x - dx) + abs(y - dy)


def solve(factor, matrix):
    """ Get distance between galaxies with a given empty space *factor*. """
    galaxies = get_galaxies(matrix)
    galaxies = expand(galaxies, factor=factor)
    return sum(distance(a, b) for a, b in itertools.combinations(galaxies, 2))


solve_pt1 = functools.partial(solve, 2)
solve_pt2 = functools.partial(solve, 1_000_000)
default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = dict(read_matrix(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
