""" Advent of Code 2018

`Day 2 <http://adventofcode.com/2018/day/2>`_:
Inventory Management System
"""
from __future__ import print_function
import argparse
import collections
import itertools
import logging


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)


def count_n(n, words):
    """ count words where at least one letter occurs n times. """
    return sum(int(n in letter_count.values())
               for letter_count in (collections.Counter(word)
                                    for word in words))


def find_letter_diff(words):
    for a, b in itertools.combinations(words, 2):
        diff = set(enumerate(a)).difference(set(enumerate(b)))
        if len(diff) == 1:
            idx, letter = diff.pop()
            logger.info("Words %r and %r differs at index %r=%r",
                        a, b, idx, letter)
            yield a, b, idx, letter


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('r'),
        default='-',
        help="file to read, or '-' to read from STDIN")
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

    words = tuple(line.strip() for line in args.file)

    if args.part_1:
        twos = count_n(2, words)
        threes = count_n(3, words)
        print("Part 1: {0} * {1} = {2}".format(twos, threes, twos * threes))

    if args.part_2:
        word_a, word_b, idx, letter = next(find_letter_diff(words))
        common = list(word_a)
        common.pop(idx)
        print("Part 2:", "".join(common))


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    main()
