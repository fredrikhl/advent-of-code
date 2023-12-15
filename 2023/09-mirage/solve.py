"""
Advent of Code 2023

`Day 9 <https://adventofcode.com/2023/day/9>`_:
Mirage Maintenance
"""
import functools
import itertools
import os
import sys


def read_input(fd):
    """ Read input from file-like *fd*. """
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            yield [int(i) for i in line.split()]
        except Exception as e:
            raise ValueError("Invalid value on line %d: %s (%s)"
                             % (lineno, repr(line), e))


def get_deltas(vector):
    """ Get deltas for a vector. """
    return [b - a for a, b in itertools.pairwise(vector)]


def get_next(vector):
    """ Predict the next number of a *vector*. """
    if vector and any(vector):
        return vector[-1] + get_next(get_deltas(vector))
    return 0


def get_prev(vector):
    """ Predict the previouos number of a *vector*. """
    if vector and any(vector):
        return vector[0] - get_prev(get_deltas(vector))
    return 0


def solve(func, values):
    return sum(func(v) for v in values)


solve_pt1 = functools.partial(solve, get_next)
solve_pt2 = functools.partial(solve, get_prev)
default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = list(read_input(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
