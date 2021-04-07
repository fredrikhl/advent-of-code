""" Advent of Code 2018

`Day 1 <http://adventofcode.com/2018/day/1>`_:
Chronal Calibration
"""
from __future__ import print_function
import argparse
import itertools
import logging


LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)


def get_deltas(filelike):
    """ parse int values from lines in a file-like object. """
    for lineno, line in enumerate(filelike, 1):
        try:
            yield int(line.strip())
        except ValueError as e:
            # Probably an empty line...
            logger.error('line %d - %s', lineno, e)
            continue


class Repeatable(object):
    """ repeatable iterator. """

    def __init__(self, it):
        self._it = it

    def __iter__(self):
        self._it, it = itertools.tee(self._it)
        return it


def find_duplicate(iterable, init=0):
    """ find first duplicate value after applying deltas from an iterator. """
    curr = init
    seen = set()
    loop = itertools.chain.from_iterable(itertools.repeat(iterable))
    for delta in loop:
        curr += delta
        if curr in seen:
            return curr
        seen.add(curr)


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

    deltas = Repeatable(iter(get_deltas(args.file)))

    if args.part_1:
        final_freq = sum(deltas)
        print("Part 1: {0}".format(final_freq))

    if args.part_2:
        first_dup = find_duplicate(deltas)
        print("Part 2: {0}".format(first_dup))


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    main()
