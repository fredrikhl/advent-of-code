""" Advent of Code 2017

`Day 3 <http://adventofcode.com/2017/day/3>`_:
Spiral Memory
"""
from __future__ import print_function, division
import argparse
import collections
import itertools


def spiral(maxitems=-1):
    """ Yield a series of square coordinates, in a reverse-clockwise spiral.

    Co-ordinate-system (x, y):

         (-1, -1)  (0, -1)  (1, -1)
         (-1,  0)  (0,  0)  (1,  0)
         (-1,  1)  (0,  1)  (1,  1)


    :param maxitems:
        Maximum number of coordinates to generate, (negative for infinite).

    :return generator:
        Returns a generator that yields co-ordinates in a spiral shape;
        (0, 0), (1, 0), (1, -1), (0, -1), ...
    """
    x = y = 0
    dx = 0
    dy = -1
    for i in itertools.count(start=1):
        if maxitems >= 0 and i > maxitems:
            break
        yield x, -y
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x + dx, y + dy


def coordinate(n):
    """ Get the co-ordinate of the nth item in a spiral. """
    x = y = 0
    for x, y in spiral(n):
        pass
    return x, y


def distance(n):
    """ Part 1: Count number of steps from (0, 0). """
    return sum(abs(z) for z in coordinate(n))


def spiral_sums(maxitems=-1):
    lut = collections.defaultdict(int)
    kernelsize = 1
    kernel = list(
        filter(
            lambda c: c != (0, 0),
            itertools.product(range(-kernelsize, kernelsize + 1), repeat=2)))

    for x, y in spiral(maxitems):
        if (x, y) == (0, 0):
            lut[(x, y)] = 1
        else:
            lut[(x, y)] = sum(lut[(x + dx, y + dy)] for dx, dy in kernel)
        yield lut[(x, y)]


def find_crossover(items):
    """ Part 2: Find item with sum > steps. """
    for value in spiral_sums():
        if value > items:
            return value


def matrix(items, start=1):
    """ Generate a matrix to visualize spiral. """
    root = items ** .5
    dimensions = int(root) + int(root % 1 > 0)

    # we need an odd number of columns and rows to center our spiral
    dimensions += int(dimensions % 2 == 0)
    dx = dimensions // 2
    dy = dimensions // 2

    m = [[0 for x in range(dimensions)] for y in range(dimensions)]
    for i, (x, y) in enumerate(spiral(items), start):
        m[y + dy][x + dx] = i
    return m


def dump_spiral(matrix, axis=True):
    digits = max(2, max(len(str(j)) for i in matrix for j in i))
    fmt = '{0}d'.format(digits)
    offset = len(matrix)//2
    sep = ' '
    hsep = '-'
    vsep = ' |'
    xsep = ' +'

    if axis:
        print(' ' * digits, end=len(vsep) * ' ')
        header = [format(m, fmt) for m in range(-offset, offset + 1)]
        print(*header, sep=sep)
        print(' ' * digits + xsep,
              end=(len(sep.join(header)) // len(hsep)) * hsep + "\n")
    for n, i in enumerate(matrix, -offset):
        if axis:
            print(format(n, fmt), end=vsep)
        row = [format(j, fmt) for j in i]
        print(*row, sep=sep)


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'number',
        type=int,
        help="input number")
    parser.add_argument(
        '-d', '--dump',
        action='store_true',
        default=False,
        help="dump the spiral matrix to STDOUT")
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

    if args.dump:
        dump_spiral(matrix(args.number))

    if args.part_1:
        print("Part 1: {0} -> {1} steps".format(args.number,
                                                distance(args.number)))

    if args.part_2:
        print("Part 2: {0} < {1}".format(args.number,
                                         find_crossover(args.number)))


if __name__ == '__main__':
    main()
