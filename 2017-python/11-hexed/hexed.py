# encoding: utf-8
""" Advent of Code 2017

`Day 11 <http://adventofcode.com/2017/day/11>`_:
Hex Ed
"""
from __future__ import print_function
import argparse
import io


EXAMPLE = u"""
ne,ne,ne
ne,ne,sw,sw
ne,ne,s,s
se,sw,se,sw,sw
""".strip()

EXAMPLE = u"""
se,sw,se,sw,sw
""".strip()

r""" A cache of hexagonally linked nodes.
      _   _   _   _   _
     / \_/ \_/ \_/ \_/ \
    | 2 | 1 | 1 | 2 | 3 |
     \ / \ / \ / \ / \ /
      | 1 | 0 | 1 | 2 |
     / \ / \ / \ / \ / \
    | 2 | 1 | 1 | 2 | 3 |
     \_/ \_/ \_/ \_/ \_/

We organize our nodes in a coordinate system, where:

 - the nw-se axis is our x-axis
 - the sw-ne axis is our y-axis

and use the coordinates to track movement:
                  _
        (y-1) SW / \ NW (x-1)
    (x+1,y-1) S |   | N (x-1,y+1)
        (x+1) SE \_/ NE (y+1)
"""

directions = {
    'ne': lambda x, y: (x, y + 1),
    'se': lambda x, y: (x + 1, y),
    'sw': lambda x, y: (x, y - 1),
    'nw': lambda x, y: (x - 1, y),
    'n': lambda x, y: (x - 1, y + 1),
    's': lambda x, y: (x + 1, y - 1),
}


def move(direction, x, y):
    return directions[direction](x, y)


def distance(x, y, target_x=0, target_y=0):
    dx, dy = target_x - x, target_y - y

    if dx * dy > 0:
        # We're not visiting a quadrant with a north/south axis, so we'll have
        # to move along the axes of out coordinate system, i.e. abs(dx) and
        # abs(dy) steps.
        return abs(dx) + abs(dy)

    # We're going to get help from the diagonal north/south axis. min(abs(dx),
    # abs(dy)) steps to the axis, and (max(abs(dx), abs(dy)) - min(abs(dx),
    # abs(dy))) to get to our target along the diagonal axis.
    return max(abs(dx), abs(dy))


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'directions',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('Ur'),
        default=io.StringIO(EXAMPLE),
        help="file with program to read, or '-' to read from STDIN")
    args = parser.parse_args(inargs)

    print('Reading directions...')
    with args.directions:
        directions = [d.strip()
                      for line in args.directions
                      for d in line.split(',')
                      if d.strip()]
    print('{0} directions read'.format(len(directions)))

    current = (0, 0)
    current_distance = max_distance = 0

    for d in directions:
        current = move(d, *current)

        current_distance = distance(*current)
        max_distance = max(current_distance, max_distance)

    print("Part 1: distance = {0}".format(current_distance))
    print("Part 2: max distance = {0}".format(max_distance))


if __name__ == '__main__':
    main()
