"""
Advent of Code 2023

`Day 8 <https://adventofcode.com/2023/day/8>`_:
Haunted Wasteland
"""
import enum
import os
import re
import sys
import math


RE_STEPS = re.compile(r"([LR]+)")
RE_TRIPLET = re.compile(r"(\w+) = \((\w+), (\w+)\)")


class PathIndex(enum.IntEnum):
    L = 0
    R = 1


def read_input(fd):
    """ Read input from file-like *fd*. """
    steps = []
    paths = []
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            m = RE_TRIPLET.match(line)
            if m:
                paths.append((m.group(1), (m.group(2), m.group(3))))
                continue
            steps.extend(int(PathIndex[i])
                         for i in RE_STEPS.match(line).group(1))
        except Exception as e:
            raise ValueError("Invalid value on line %d: %s (%s)"
                             % (lineno, repr(line), e))
    return steps, dict(paths)


def repeat(sequence):
    while True:
        for item in sequence:
            yield item


class Network(object):

    def __init__(self, instructions, connections):
        self.connections = connections
        self.instructions = instructions

    def get_length(self, current, match_target):
        count = 0
        for inst in repeat(self.instructions):
            if match_target(current):
                return count
            current = self.connections[current][inst]
            count += 1

    def __call__(self, match_start, match_target):
        initial = [n for n in self.connections if match_start(n)]
        if not initial:
            return -1
        # In my head this should only work if all the target nodes wrapped
        # around to the initial nodes, which they don't.  It seems to work
        # though...
        lengths = [self.get_length(n, match_target)
                   for n in initial]
        return math.lcm(*lengths)


def solve_pt1(values):
    solve = Network(*values)
    return solve(lambda n: n == "AAA", lambda n: n == "ZZZ")


def solve_pt2(values):
    solve = Network(*values)
    return solve(lambda n: n[-1] == "A", lambda n: n[-1] == "Z")


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
