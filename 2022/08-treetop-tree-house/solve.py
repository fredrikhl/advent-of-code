""" Advent of Code 2022

`Day 8 <https://adventofcode.com/2022/day/8>`_:
Treetop Tree House
"""
import functools
import operator
import os
import sys


def read_input(fd):
    """ Read position and height pairs from file-like *fd*. """
    rownum = 0
    for lineno, line in enumerate(fd, 1):
        if not line.strip():
            continue
        try:
            row = tuple(int(d) for d in line.strip())
            for colnum, digit in enumerate(row):
                yield (rownum, colnum), digit
            rownum += 1
        except Exception as e:
            raise ValueError('invalid input on line %d (%r): %s'
                             % (lineno, line, e))


# Deltas for moving in a given direction: up, left, right, down
DIRECTIONS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def get_path(matrix, point, delta):
    """ Iterate over tree heights from *point*, moving with *delta*. """
    point = (point[0] + delta[0], point[1] + delta[1])
    while point in matrix:
        yield matrix[point]
        point = (point[0] + delta[0], point[1] + delta[1])


def get_paths(matrix, point):
    """ Get iterables over tree heights in all directions from *point*. """
    for delta in DIRECTIONS:
        yield get_path(matrix, point, delta)


def is_visible(matrix, point):
    """ Check if tree at *point* is visible from edges. """
    height = matrix[point]
    for path in get_paths(matrix, point):
        if all(h < height for h in path):
            # All lower trees on this path
            return True
    return False


def solve_pt1(matrix):
    return sum(is_visible(matrix, p) for p in matrix)


def get_view_distance(path, height):
    """ Get view distance in a given *path*. """
    count = 0
    for count, h in enumerate(path, 1):
        if h >= height:
            break
    return count


def get_view_score(matrix, point):
    """ Calculate view score at a given *point*. """
    height = matrix[point]
    distances = (get_view_distance(path, height)
                 for path in get_paths(matrix, point))
    return functools.reduce(operator.mul, distances, 1)


def solve_pt2(matrix):
    return max(get_view_score(matrix, p) for p in matrix)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = dict(read_input(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
