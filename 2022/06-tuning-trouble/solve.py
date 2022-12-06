""" Advent of Code 2022

`Day 6 <https://adventofcode.com/2022/day/6>`_:
Tuning Trouble
"""
import collections
import functools
import itertools
import os
import sys


def read_line(fd):
    """ Get next non-empty line from file-like. """
    for line in (ln.rstrip() for ln in fd):
        if line:
            return line
    raise ValueError("no remaining lines in: " + repr(fd))


def sliding_window(iterable, size):
    """ Get an iterable sliding window of *size* over *iterable*. """
    iterable = iter(iterable)

    window = collections.deque(itertools.islice(iterable, size), maxlen=size)
    if len(window) == size:
        yield tuple(window)

    for item in iterable:
        window.append(item)
        yield tuple(window)


def solve(stream, size):
    """ Find marker of *size* unique values in *stream*. """
    for i, window in enumerate(sliding_window(stream, size), size):
        if len(set(window)) == size:
            # *size* unique items in window, at stream position *i*
            return i
    raise RuntimeError("no unique marker found of size: " + repr(size))


solve_pt1 = functools.partial(solve, size=4)
solve_pt2 = functools.partial(solve, size=14)
default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            stream = read_line(f)

        pt1 = solve_pt1(stream)
        print('Part 1:', pt1)

        pt2 = solve_pt2(stream)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
