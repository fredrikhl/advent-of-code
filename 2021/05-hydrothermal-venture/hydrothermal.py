""" Advent of Code 2021

`Day 5 <http://adventofcode.com/2021/day/5>`_:
Hydrothermal venture
"""
import collections
import os
import sys


def parse_point(value):
    _, _ = p = tuple(int(v.strip()) for v in value.split(','))
    return p


def parse_line(value):
    a, _, b = value.strip().partition(' -> ')
    return parse_point(a), parse_point(b)


def read_lines(fd):
    for lineno, line in enumerate(fd, 1):
        try:
            yield parse_line(line.strip())
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def next_value(c, e):
    """ get a value from *c* that is 1 closer to *e*. """
    return c + (c < e) - (c > e)


def iter_points(line):
    """ get all points along a *line*. """
    cur, end = line
    yield cur

    while cur != end:
        cur = tuple(next_value(*a) for a in zip(cur, end))
        yield cur


def count_overlaps(points):
    """ count number of overlapping *points*. """
    counter = collections.Counter()
    for p in points:
        counter[p] += 1
    return sum(v > 1 for v in counter.values())


def filter_out_diagonal(lines):
    """ get all *lines* that are parallel to an axis. """
    for line in lines:
        if any(a == b for a, b in zip(*line)):
            yield line


def solve_pt1(all_lines):
    lines = tuple(filter_out_diagonal(all_lines))
    points = (p for v in lines for p in iter_points(v))
    return count_overlaps(points)


def solve_pt2(lines):
    points = (p for v in lines for p in iter_points(v))
    return count_overlaps(points)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            lines = tuple(read_lines(f))

        pt1 = solve_pt1(lines)
        print('Part 1:', pt1)
        pt2 = solve_pt2(lines)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
