""" Advent of Code 2022

`Day 3 <https://adventofcode.com/2022/day/3>`_:
Rucksack Reorganization
"""
import collections
import functools
import itertools
import os
import string
import sys


# Map of intentory characters to priority
PRIORITY_MAP = {
    char: value
    for value, char
    in enumerate(string.ascii_lowercase + string.ascii_uppercase, 1)}


# A set of all valid intentory items (characters)
VALID_ITEMS = set(PRIORITY_MAP.keys())


def read_lines(fd):
    """ Read rucksack content from file. """
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        invalid_items = set(line) - VALID_ITEMS
        if invalid_items:
            raise ValueError("Invalid values on line %d: %r (%r)"
                             % (lineno, "".join(invalid_items), line))
        yield line


def sum_priority(items):
    """ Sum items by priority. """
    return sum(PRIORITY_MAP[item] for item in items)


def find_common_item(groups):
    """ Find common item in groups of items. """
    sets = (set(g) for g in groups)
    common_items = functools.reduce(set.intersection, sets, VALID_ITEMS)
    if len(common_items) != 1:
        raise ValueError("Found %d common items in: %r"
                         % (len(common_items), groups))
    return common_items.pop()


def find_compartment_items(rucksacks):
    """ Find each item shared between rucksack compartments. """
    for rucksack in rucksacks:
        split = len(rucksack) // 2
        compartments = (rucksack[:split], rucksack[split:])
        yield find_common_item(compartments)


def solve_pt1(inventory):
    return sum_priority(find_compartment_items(inventory))


def find_triplet_items(rucksacks):
    """ Find common item in each group of three rucksacks. """
    it = iter(rucksacks)
    while (triplet := tuple(itertools.islice(it, 3))):
        yield find_common_item(triplet)


def solve_pt2(inventory):
    return sum_priority(find_triplet_items(inventory))


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = tuple(read_lines(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
