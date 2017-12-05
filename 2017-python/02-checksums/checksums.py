""" Advent of Code 2017

`Day 2 <http://adventofcode.com/2017/day/2>`_:
Corruption Checksum
"""
from __future__ import absolute_import, print_function, division
import argparse
import itertools


def parse_spreadsheet(text):
    """ Parse text into rows of numbers. """
    for line in text.splitlines():
        line = line.strip(' ')
        if not line:
            continue
        yield [int(col) for col in line.split() if col.strip()]


def sum_diff(lines):
    """ Part 1: Sum of min/max diff in each row. """
    total = 0
    for nums in lines:
        total += max(nums) - min(nums)
    return total


def find_divisible(numbers):
    """ Find two evenly divisible numbers in a list of numbers. """
    for a, b in itertools.permutations(set(numbers), 2):
        if a < b:
            continue
        if a % b == 0:
            return a // b
    raise ValueError("no divisible numbers")


def sum_divisible(lines):
    """ Part 2: Sum of division results in each row. """
    total = 0
    for nums in lines:
        total += find_divisible(nums)
    return total


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'spreadsheet',
        metavar='FILE',
        type=argparse.FileType('Ur'),
        help="file with digits to read, or '-' to read from STDIN")
    skip = parser.add_mutually_exclusive_group()
    skip.add_argument(
        '--skip-part-1',
        dest='part_1',
        action='store_false',
        default=True,
        help="skip part 1")
    skip.add_argument(
        '--skip-part-2',
        dest='part_2',
        action='store_false',
        default=True,
        help="skip part 2")
    args = parser.parse_args(inargs)

    print('Reading spreadsheet...')
    with args.spreadsheet as f:
        data = parse_spreadsheet(f.read())
    print('done')

    p1, p2 = itertools.tee(data)

    if args.part_1:
        print("Part 1: {0}".format(sum_diff(p1)))

    if args.part_2:
        print("Part 2: {0}".format(sum_divisible(p2)))


if __name__ == '__main__':
    main()
