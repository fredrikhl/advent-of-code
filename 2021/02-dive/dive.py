""" Advent of Code 2021

`Day 2 <http://adventofcode.com/2021/day/2>`_:
Dive!
"""
import functools
import os
import sys


DIRECTIONS = {
    'forward': (1, 0),
    'up': (0, -1),
    'down': (0, 1),
}


def parse_op(value):
    d, _, f = (s.strip() for s in value.strip().partition(' '))
    return tuple(int(f) * v for v in DIRECTIONS[d])


def read_ops(fd):
    for lineno, line in enumerate(fd, 1):
        try:
            yield parse_op(line)
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def next_pos(current, op):
    return tuple(sum(t) for t in zip(current, op))


def next_aim(current, op):
    h, aim = next_pos(current[:2], op)
    d = current[2] + op[0] * aim
    return (h, aim, d)


def solve_pt1(ops):
    h, d = functools.reduce(next_pos, ops, (0, 0))
    return h * d


def solve_pt2(ops):
    h, _, d = functools.reduce(next_aim, ops, (0, 0, 0))
    return h * d


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            ops = tuple(read_ops(f))

        pt1 = solve_pt1(ops)
        print('Part 1:', pt1)
        pt2 = solve_pt2(ops)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
