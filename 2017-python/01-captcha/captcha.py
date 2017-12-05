""" Advent of Code 2017

`Day 1 <http://adventofcode.com/2017/day/1>`_:
Inverse Captcha
"""
from __future__ import division, print_function
import argparse


def offset_summer(offset, digits):
    """ Part 1: Sum digit if digit + offset matches. """
    digits = str(int(digits))
    total = 0
    for next_idx, digit in enumerate(digits, offset):
        if digit == digits[next_idx % len(digits)]:
            total += int(digit)
    return total


def divisible_offset_summer(divisor, digits):
    """ Part 2: Sum digit if digit + offset matches. """
    digits = str(int(digits))
    if len(digits) % divisor != 0:
        raise ValueError("need even number of digits")
    return offset_summer(len(digits) // divisor, digits)


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'digits',
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

    print('Reading digits...')
    with args.digits:
        digits = args.digits.readline().strip()
    print('{0} digits read'.format(len(digits)))

    if args.part_1:
        print("Part 1:", offset_summer(1, digits))

    if args.part_2:
        print("Part 2:", divisible_offset_summer(2, digits))


if __name__ == '__main__':
    main()
