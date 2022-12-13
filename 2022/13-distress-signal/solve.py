""" Advent of Code 2022

`Day 13 <https://adventofcode.com/2022/day/13>`_:
Distress Signal
"""
import functools
import json
import operator
import os
import sys
import itertools


def read_input(fd):
    """ Read and parse list pairs from file. """
    lines = iter(enumerate(fd, 1))
    lineno = 0
    line = ""
    while (triplet := tuple(itertools.islice(lines, 3))):
        try:
            lineno, line = triplet[0]
            a = json.loads(line)
            lineno, line = triplet[1]
            b = json.loads(line)
            yield a, b

            if len(triplet) < 3:
                # done - only got 2 lines in triplet
                break
            lineno, line = triplet[2]
            if line != "\n":
                raise ValueError("expected empty line")
        except Exception as e:
            raise ValueError("invalid value on line %d (%r): %s" %
                             (lineno, line, e))


def compare(left, right):
    """ cmp-style function for input pairs. """
    if all(isinstance(v, int) for v in (left, right)):
        return (left > right) - (left < right)

    if all(isinstance(v, list) for v in (left, right)):
        for args in zip(left, right):
            if (c := compare(*args)) != 0:
                return c
        return compare(len(left), len(right))

    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)

    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])

    raise ValueError("invalid values: %r, %r" % (left, right))


def solve_pt1(pairs):
    return sum(i for i, pair in enumerate(pairs, 1)
               if compare(*pair) < 0)


def solve_pt2(pairs):
    dividers = ([[2]], [[6]])
    items = [item for pair in pairs for item in pair]
    if any(d in items for d in dividers):
        raise RuntimeError("dividers already present in input")

    items.extend(dividers)
    items.sort(key=functools.cmp_to_key(compare))
    indices = (items.index(i) + 1 for i in dividers)
    return functools.reduce(operator.mul, indices, 1)


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            values = tuple(read_input(f))

        pt1 = solve_pt1(values)
        print("Part 1:", pt1)

        pt2 = solve_pt2(values)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
