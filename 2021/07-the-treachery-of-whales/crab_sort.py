""" Advent of Code 2021

`Day 7 <http://adventofcode.com/2021/day/7>`_:
The Treachery of Whales
"""
import operator
import os
import sys


def read_state(fd):
    """ read current crab state from file-like *fd*. """
    for lineno, line in enumerate(fd, 1):
        if not line.strip():
            continue
        try:
            return tuple(int(v.strip()) for v in line.split(','))
        except Exception as e:
            raise ValueError('invalid values on line %d (%r): %s' %
                             (lineno, line, e))


def find_lowest_score(positions, get_score):
    """
    :param positions: current crab positions
    :param get_score: callable get_score(positions, target_position) -> score
    """
    candidates = (range(1, len(positions) + 1))
    return min(
        ((target, get_score(positions, target)) for target in candidates),
        key=operator.itemgetter(1),
    )


def get_align_score(positions, target):
    return sum(abs(n - target) for n in positions)


def solve_pt1(positions):
    min_n, min_score = find_lowest_score(positions, get_align_score)
    return min_score


def get_tri_score(positions, target):
    return sum(sum(range(abs(n - target) + 1)) for n in positions)


def solve_pt2(positions):
    min_n, min_score = find_lowest_score(positions, get_tri_score)
    return min_score


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            initial = read_state(f)

        pt1 = solve_pt1(initial)
        print('Part 1:', pt1)

        pt2 = solve_pt2(initial)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
