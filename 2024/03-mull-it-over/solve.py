"""
Advent of Code 2024

`Day 3 <https://adventofcode.com/2024/day/3>`_:
Mull It Over
"""
import re
import operator
import os
import sys


INSTRUCTION_REGEX = re.compile(
    r"""
    mul\((\d{1,3}),(\d{1,3})\)
    | do\(\)
    | don't\(\)
    """,
    re.VERBOSE,
)


def parse_line(line, offset=0):
    """ find valid instructions in a *line*, starting at *offset* """
    while offset < len(line):
        m = INSTRUCTION_REGEX.match(line[offset:])
        if not m:
            offset += 1
            continue
        if m.string.startswith("mul("):
            yield "mul", tuple(int(v) for v in m.groups())
        elif m.string.startswith("do("):
            yield "enable", True
        elif m.string.startswith("don't("):
            yield "enable", False
        assert (end := m.end()) > 0
        offset += end


def read_input(f):
    """ find operations and arguments from file-like *f* """
    for lineno, raw_line in enumerate(f, 1):
        line = raw_line.strip()
        if not line:
            continue
        yield from parse_line(line)


def solve_pt1(items):
    """ get the sum of all valid mul() instructions """
    return sum(operator.mul(*args) for op, args in items if op == "mul")


def filter_enabled(items, enabled=True):
    """ find all enabled instructions in *items* """
    for op, args in items:
        if op == "enable":
            enabled = args
        elif enabled:
            yield op, args


def solve_pt2(items):
    """ get the sum of all enabled mul() instructions """
    return solve_pt1(filter_enabled(items))


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            items = list(read_input(f))

        pt1 = solve_pt1(items)
        print('Part 1:', pt1)

        pt2 = solve_pt2(items)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
