""" Advent of Code 2021

`Day 1 <http://adventofcode.com/2021/day/1>`_:
Sonar Sweep
"""
import collections
import itertools
import os
import sys


def read_numbers(fd):
    for lineno, line in enumerate(fd, 1):
        try:
            yield int(line.strip())
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def get_deltas(iterable):
    iterable = iter(iterable)
    prev = next(iterable)
    for curr in iterable:
        yield curr - prev
        prev = curr


def count_incr(iterable):
    return sum(d > 0 for d in get_deltas(iterable))


def sliding_window(iterable, size):
    iterable = iter(iterable)

    window = collections.deque(itertools.islice(iterable, size), maxlen=size)
    if len(window) == size:
        yield tuple(window)

    for item in iterable:
        window.append(item)
        yield tuple(window)


def sliding_sums(iterable, size):
    """ sum of each group in a sliding window of numbers. """
    return (sum(group) for group in sliding_window(iterable, size))


solve_pt1 = count_incr


def solve_pt2(numbers):
    return count_incr(sliding_sums(numbers, 3))


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            numbers = tuple(read_numbers(f))

        pt1 = solve_pt1(numbers)
        print('Part 1:', pt1)

        pt2 = solve_pt2(numbers)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
