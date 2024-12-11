"""
Advent of Code 2024

`Day 8 <https://adventofcode.com/2024/day/8>`_:
Resonant Collinearity
"""
import collections
import itertools
import os
import sys


def read_map(f):
    """ read position and letter pairs from file-like *f*. """
    rownum = 0
    for lineno, line in enumerate(f, 1):
        if not line.strip():
            continue
        for colnum, char in enumerate(line.strip()):
            yield ((rownum, colnum), char)
        rownum += 1


def get_antenna_pairs(antenna_map, ignore="."):
    """ get pairs of antennas that share the same frequency. """
    frequency_groups = collections.defaultdict(set)
    for point, freq in antenna_map.items():
        if freq in ignore:
            continue
        frequency_groups[freq].add(point)

    for points in frequency_groups.values():
        if len(points) < 2:
            continue
        yield from itertools.permutations(points, 2)


def generate_antinodes(a, b):
    """ find points in a line from *a*, in the opposite direction of *b*. """
    delta = (a[0] - b[0], a[1] - b[1])
    while True:
        a = (a[0] + delta[0], a[1] + delta[1])
        yield a


def get_next_antinodes(antenna_map):
    """ get the next antinode for all antennas in the *antenna_map* """
    for a, b in get_antenna_pairs(antenna_map):
        c = next(generate_antinodes(a, b))
        if c in antenna_map:
            yield c


def get_all_antinodes(antenna_map):
    """ get all antinodes in the *antenna_map* """
    for a, b in get_antenna_pairs(antenna_map):
        antinodes = generate_antinodes(a, b)
        while a in antenna_map:
            yield a
            a = next(antinodes)


def solve_pt1(antenna_map):
    return len(set(get_next_antinodes(antenna_map)))


def solve_pt2(antenna_map):
    return len(set(get_all_antinodes(antenna_map)))


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            antenna_map = dict(read_map(f))

        pt1 = solve_pt1(antenna_map)
        print("Part 1:", pt1)

        pt2 = solve_pt2(antenna_map)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
