""" Advent of Code 2022

`Day 4 <https://adventofcode.com/2022/day/4>`_:
Camp Cleanup
"""
import re
import os
import sys


class Range(object):
    """ A range object for checking full/partial overlap with other ranges. """

    def __init__(self, start, stop):
        self.start, self.stop = int(start), int(stop)
        if self.start > self.stop:
            raise ValueError("start=%r > stop=%r" % (self.start, self.stop))

    def __contains__(self, other):
        """ Check if *self* fully contains *other*. """
        return self.start <= other.start and self.stop >= other.stop

    def __lt__(self, other):
        """ Check if all of *self* stops before *other*. """
        return self.stop < other.start

    def __gt__(self, other):
        """ Check if all of *self* starts after *other*. """
        return self.start > other.stop

    def full_overlap_with(self, other):
        return self in other or other in self

    def partial_overlap_with(self, other):
        return not (self < other or self > other)


RE_LINE = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def parse_line(line):
    """ Get a pair of Range objects from an input line. """
    a, b, c, d = RE_LINE.match(line.strip()).groups()
    return Range(a, b), Range(c, d)


def read_values(fd):
    """ Read sector id range pairs from file-like. """
    for lineno, line in enumerate(fd, 1):
        try:
            yield parse_line(line)
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def solve_pt1(range_pairs):
    return sum(a.full_overlap_with(b) for a, b in range_pairs)


def solve_pt2(range_pairs):
    return sum(a.partial_overlap_with(b) for a, b in range_pairs)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = tuple(read_values(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
