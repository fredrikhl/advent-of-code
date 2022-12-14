""" Advent of Code 2022

`Day 14 <https://adventofcode.com/2022/day/14>`_:
Regolith Reservoir
"""
import functools
import itertools
import os
import sys

X, Y = 0, 1
SPAWN = (500, 0)


def read_input(fd):
    """ Read and parse polygonal chains from file. """
    for lineno, raw_line in enumerate(fd, 1):
        if not (line := raw_line.strip()):
            continue
        try:
            points = (p.split(',', 1)
                      for p in line.split(" -> "))
            yield tuple((int(p[X]), int(p[Y])) for p in points)
        except Exception as e:
            raise ValueError("invalid value on line %d (%r): %s" %
                             (lineno, line, e))


def fill_lines(lines):
    """ Create wall points from line segment vertices. """
    for line in lines:
        for a, b in itertools.pairwise(line):
            if b < a:
                a, b = b, a
            if a[X] == b[X]:
                for y in range(a[Y], b[Y] + 1):
                    yield (a[X], y)
            elif a[Y] == b[Y]:
                for x in range(a[X], b[X] + 1):
                    yield (x, a[Y])
            else:
                raise ValueError("not a straight line: %r -> %r" % (a, b))


def solve(lines, abyss):
    walls = set(fill_lines(lines))
    bottom = max(p[Y] for p in walls) + 1

    def next_pos(curr):
        """ Find next position for a unit of sand at position *curr*. """
        x, y = curr
        candidates = ((x, y + 1), (x - 1, y + 1), (x + 1, y + 1))
        for p in candidates:
            if p not in walls:
                return p
        return curr

    def drop(curr):
        """ Drop a unit of sand at position *curr* and see where it lands. """
        while True:
            prev, curr = curr, next_pos(curr)
            if prev == curr:
                return curr
            elif curr[Y] == bottom:
                return curr

    # Count units of sand until no more sand can land
    sands = 0
    while True:
        pos = drop(SPAWN)
        if abyss and pos[Y] == bottom:
            # done: sand didn't land anywhere
            break
        sands += 1
        walls.add(pos)
        if pos == SPAWN:
            # done: previous position blocks the spawn point
            break
    return sands


solve_pt1 = functools.partial(solve, abyss=True)
solve_pt2 = functools.partial(solve, abyss=False)
default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            values = tuple(read_input(f))

        pt1 = solve_pt1(values)
        print("Part 1:", pt1)

        pt2 = solve_pt2(values)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
