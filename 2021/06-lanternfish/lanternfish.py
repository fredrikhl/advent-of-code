""" Advent of Code 2021

`Day 6 <http://adventofcode.com/2021/day/6>`_:
Lanternfish
"""
import collections
import os
import sys

NEW_DAYS_LEFT = 8
RST_DAYS_LEFT = 6


def read_counts(fd):
    """ read fish counts from a file-like *fd*. """
    for lineno, line in enumerate(fd, 1):
        if not line.strip():
            continue
        try:
            return tuple(int(v.strip()) for v in line.split(','))
        except Exception as e:
            raise ValueError('invalid values on line %d (%r): %s' %
                             (lineno, line, e))


def new_state(initial):
    """ convert *initial* counts to a state deque. """
    size = NEW_DAYS_LEFT + 1
    by_days = collections.Counter(initial)
    values = (by_days[days] for days in range(size))
    return collections.deque(values, size)


def next_state(curr):
    """ get next day state from *curr* state deque. """
    new = collections.deque(curr, NEW_DAYS_LEFT + 1)
    new.rotate(-1)
    new[RST_DAYS_LEFT] += new[-1]
    return new


def get_state(initial, n):
    """ get state deque after *n* days from *initial* counts. """
    curr = new_state(initial)
    for i in range(n):
        curr = next_state(curr)
    return curr


def solve_pt1(initial):
    return sum(get_state(initial, 80))


def solve_pt2(initial):
    return sum(get_state(initial, 256))


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            initial = tuple(read_counts(f))

        pt1 = solve_pt1(initial)
        print('Part 1:', pt1)
        pt2 = solve_pt2(initial)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
