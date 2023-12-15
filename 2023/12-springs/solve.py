"""
Advent of Code 2023

`Day 12 <https://adventofcode.com/2023/day/12>`_:
Hot Springs
"""
import functools
import os
import re
import sys


RE_LINE = re.compile(r"^([#.?]+) ([0-9,]+)$")


def parse_line(value):
    springs, raw_counts = RE_LINE.match(value).groups()
    counts = tuple(int(c) for c in raw_counts.split(","))
    return springs, counts


def read_input(fd):
    """ Read input from file-like *fd*. """
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            yield parse_line(line)
        except Exception as e:
            raise ValueError("Invalid value on line %d: %s (%s)"
                             % (lineno, repr(line), e))


@functools.cache
def count_matches(springs, conditions):
    if len(springs) == 0:
        # no springs - this is a valid case if we don't have any conditions
        return not conditions or conditions == (0,)

    if conditions and conditions[0] < 0:
        # current condition is broken
        return 0

    if springs[0:2] == "#.":
        # A change from group to non-group:  If the current condition is
        # satisfied, we can continue with the next group.
        if conditions and conditions[0] == 1:
            return count_matches(springs[1:], conditions[1:])
        return 0

    if springs[0:2] == "#?":
        # We need to check if this *could* be a group to non-group case
        return (
            count_matches("#." + springs[2:], conditions)
            + count_matches("##" + springs[2:], conditions)
        )

    if springs[0] == "#":
        # decrement current condition
        if conditions:
            conditions = (conditions[0] - 1,) + conditions[1:]
            return count_matches(springs[1:], conditions)
        return 0

    if springs[0] == "?":
        return (
            count_matches("." + springs[1:], conditions)
            + count_matches("#" + springs[1:], conditions)
        )

    return count_matches(springs[1:], conditions)


def solve(values):
    return sum(count_matches(springs, conditions)
               for springs, conditions in values)


def solve_pt1(values):
    return solve(values)


def solve_pt2(values):
    values = [
        ("?".join((springs,) * 5), conds * 5)
        for springs, conds in values]
    return solve(values)


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
