""" Advent of Code 2017

`Day 6 <http://adventofcode.com/2017/day/6>`_:
Memory Reallocation
"""
from __future__ import division, print_function
import argparse
import collections
import io
import itertools


EXAMPLE = u"\t".join(str(i) for i in (0, 2, 7, 0))


def cycle(banks):
    """ Perform one cycle of redistribution.

    Given a list or sequence of numbers, this function will take the first,
    highest number, and re-distribute it across the other numbers in the list.

    :param iterable banks:
        A list of banks and their number of blocks.

    :return list:
        Returns the new state as a list.
    """
    banks = list(banks)

    # elect bank
    max_value = max(banks)
    max_idx = banks.index(max_value)

    # update banks
    banks[max_idx] -= max_value
    for i in range(1, max_value + 1):
        banks[(max_idx + i) % len(banks)] += 1

    return banks


def redistribute(initial, limit=1):
    """ Run distribution cycle until a duplicate set of banks is seen.

    Runs the cycle until a duplicate set of banks is seen for the n-th time.

    :param list initial:
        The initial set of banks.

    :param int limit:
        How many times the same set of banks is encountered before stopping.

    :return generator:
        Returns a generator that yields tuples with:

        - total cycle count
        - cycle count (since start, or since last encounter with the same bank)
        - list of current banks
    """
    seen = collections.defaultdict(lambda: 0)
    bank = initial
    interval = interval_cycles = 0
    for total_cycles in itertools.count(0):
        seen[tuple(bank)] += 1
        yield total_cycles, interval_cycles, bank

        # reset interval if seen, or increment interval count
        if seen[tuple(bank)] > interval:
            interval += 1
            interval_cycles = 1
        else:
            interval_cycles += 1

        # end if interval count has reached its limit
        if seen[tuple(bank)] > limit:
            break

        bank = cycle(bank)


def count(iterable):
    """ Get the number of cycles in a redistribute generator. """
    for _, i, _ in iterable:
        pass
    return i


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'initial',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('Ur'),
        default=io.StringIO(EXAMPLE),
        help="file with banks to read, or '-' to read from STDIN")
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

    print('Reading banks...')
    with args.initial:
        initial = [int(i) for i in args.initial.readline().split() if i]
    print('{0} banks read'.format(len(initial)))

    if args.part_1:
        print("Part 1:", count(redistribute(initial, 1)))

    if args.part_2:
        print("Part 2:", count(redistribute(initial, 2)))


if __name__ == '__main__':
    main()
