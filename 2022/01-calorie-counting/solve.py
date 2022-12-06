""" Advent of Code 2022

`Day 1 <https://adventofcode.com/2022/day/1>`_:
Calorie Counting
"""
import collections
import functools
import os
import sys


def read_inventory(fd):
    """ Read calorie counts from file-like. """
    current_group = 0
    new_group = True

    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            new_group = True
            continue

        if new_group:
            current_group += 1
            new_group = False
        try:
            yield current_group, int(line)
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def get_calorie_count(inventory_pairs):
    """ Sum up total calories per elf. """
    c = collections.Counter()
    for elfnum, calories in inventory_pairs:
        c[elfnum] += calories
    return c


def solve(count, top_n):
    """ Count calories carried by the *top_n* calorie heavy elves. """
    return sum(calories for elfnum, calories in count.most_common(top_n))


solve_pt1 = functools.partial(solve, top_n=1)
solve_pt2 = functools.partial(solve, top_n=3)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            calories = get_calorie_count(read_inventory(f))

        pt1 = solve_pt1(calories)
        print('Part 1:', pt1)

        pt2 = solve_pt2(calories)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
