""" Advent of Code 2018

`Day 3 <http://adventofcode.com/2018/day/2>`_:
No Matter How You Slice It
"""
from __future__ import print_function
import argparse
import io
import collections
import itertools
import logging


EXAMPLE = u"""
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
""".strip()

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)


def generate_points(a, b):
    for x in range(a.x, b.x):
        for y in range(a.y, b.y):
            yield Vector(x, y)


class Vector(object):
    """ a simple vector, with x and y offsets. """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '{cls.__name__}({obj.x}, {obj.y})'.format(cls=type(self),
                                                         obj=self)

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __bool__(self):
        return self.x != 0 and self.y != 0

    def __nonzero__(self):
        # PY2
        return self.__bool__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Rect(object):
    """ a rectangle represented by an offset vector and a size vector. """

    def __init__(self, offset, size):
        self.offset = offset
        self.size = size

    def intersection(self, other):
        offset = Vector(max(self.offset.x, other.offset.x),
                        max(self.offset.y, other.offset.y))
        self_opposite = self.offset + self.size
        other_opposite = other.offset + other.size
        size = Vector(
            max(0, min(self_opposite.x, other_opposite.x) - offset.x),
            max(0, min(self_opposite.y, other_opposite.y) - offset.y))
        return type(self)(offset, size)

    def __eq__(self, other):
        return self.offset == other.offset and self.size == other.size

    def __contains__(self, other):
        return self.intersection(other) == other

    def __repr__(self):
        return ('{cls.__name__}('
                '{obj.offset!r}, {obj.size!r})'
                ).format(cls=type(self), obj=self)


class Claim(object):

    def __init__(self, ident, rectangle):
        self.ident = str(ident)
        self.rectangle = rectangle

    def __repr__(self):
        return ('{cls.__name__}('
                '{obj.ident}, ({obj.rectangle!r})'
                ).format(cls=type(self), obj=self)

    def __str__(self):
        return ('#{0.ident} @ {0.rectangle.offset.x},{0.rectangle.offset.y}: '
                '{0.rectangle.size.x}x{0.rectangle.size.y}').format(self)

    @classmethod
    def from_str(cls, s):
        s, _, sz = s.partition(': ')
        w, _, h = sz.partition('x')
        s, _, dv = s.partition(' @ ')
        x, _, y = dv.partition(',')
        ident = int(s.lstrip('#'))
        offset = Vector(int(x), int(y))
        size = Vector(int(w), int(h))
        return cls(ident, Rect(offset, size))


def get_claims(filelike):
    for lineno, line in enumerate(filelike, 1):
        try:
            yield Claim.from_str(line.strip())
        except Exception:
            logger.error('line %d', lineno, exc_info=True)
            continue


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('r'),
        default=io.StringIO(EXAMPLE),
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

    claims = list(get_claims(args.file))

    if args.part_1:
        fabric = collections.Counter()
        for rect in (c.rectangle for c in claims):
            for point in generate_points(rect.offset, rect.offset + rect.size):
                fabric[point.x, point.y] += 1

        overlapping = list(filter(lambda v: v[1] >= 2, fabric.items()))
        print('Part 1:', len(overlapping))

    if args.part_2:
        non_overlapping = claims[:]
        for a, b in itertools.combinations(claims, 2):
            overlap = a.rectangle.intersection(b.rectangle)
            if bool(overlap.size):
                for c in (a, b):
                    if c in non_overlapping:
                        non_overlapping.remove(c)
        print('Part 2:', map(str, non_overlapping))


if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    main()
