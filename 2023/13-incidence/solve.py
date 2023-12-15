"""
Advent of Code 2023

`Day 13 <https://adventofcode.com/2023/day/13>`_:
Point of Incidence
"""
import functools
import itertools
import os
import sys


def read_input(fd):
    """ Read input from file-like *fd*. """
    buffer = []
    expect = 0
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            if buffer:
                yield buffer
            buffer = []
            expect = 0
            continue
        linelen = len(line)
        try:
            if expect and linelen != expect:
                raise ValueError("too many chars (%d, expeced %d)"
                                 % (linelen, expect))
            buffer.append(line)
        except Exception as e:
            raise ValueError("Invalid value on line %d: %s (%s)"
                             % (lineno, repr(line), e))
        expect = linelen
    if buffer:
        yield buffer


def flip(rows):
    flipped = []
    length = len(rows[0])
    for i in range(length):
        flipped.append("".join(row[i] for row in rows))
    return flipped


def difference(row_a, row_b):
    return sum(col_a != col_b for col_a, col_b in zip(row_a, row_b))


def is_reflection_line(mirror, line, smudges=0):
    """
    Validate a potential reflection line.

    :param mirror: list of mirror rows
    :param line: index of the first row *after* the reflection line
    :param smudges: number of smudges to expect on the mirror
    """
    a, b = line - 1, line
    while (a >= 0 and b < len(mirror)):
        diff = difference(mirror[a], mirror[b])
        if diff > smudges:
            # too many differences
            return False
        smudges -= diff
        a, b = a - 1, b + 1

    if smudges > 0:
        # too few differences
        return False
    return True


def find_reflection_lines(mirror, smudges=0):
    """
    Find reflection lines in a given mirror.

    :param mirror: list of mirror rows
    :param smudges: number of smudges to expect on the mirror
    """
    for line, (a, b) in enumerate(itertools.pairwise(mirror), 1):
        if (difference(a, b) <= smudges
                and is_reflection_line(mirror, line, smudges)):
            yield line


def get_mirror_value(mirror, smudges=0):
    for horizontal_line in find_reflection_lines(mirror, smudges):
        return horizontal_line * 100

    for vertical_line in find_reflection_lines(flip(mirror), smudges):
        return vertical_line

    raise ValueError("no reflection line")


def solve(smudges, values):
    return sum(get_mirror_value(mirror, smudges) for mirror in values)


solve_pt1 = functools.partial(solve, 0)
solve_pt2 = functools.partial(solve, 1)
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
