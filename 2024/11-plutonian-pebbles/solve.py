"""
Advent of Code 2024

`Day 11 <https://adventofcode.com/2024/day/11>`_:
Plutonian Pebbles
"""
import collections
import functools
import os
import sys


def read_input(f):
    """ read the numbers from a file-like *f*. """
    for lineno, line in enumerate(f, 1):
        try:
            for value in line.strip().split():
                yield int(value)
        except Exception as e:
            raise ValueError("invalid input on line %d: %s" % (lineno, e))


def change_stone(value):
    """ get new stone engraving(s) for a given engraving *value* """
    if value == 0:
        return (1,)
    digits = len(str(value))
    if digits % 2 == 0:
        factor = 10 ** (digits // 2)
        return (value // factor, value % factor)
    return (value * 2024,)


def next_stone_count(oldcount):
    """ get new stone counts from *oldcount* after a single blink. """
    newcount = collections.defaultdict(int)
    for stone, stone_count in oldcount.items():
        for new_stone in change_stone(stone):
            newcount[new_stone] += stone_count
    return newcount


def solve(stones, blinks):
    """ get number of stones after *limit* blinks """
    stone_count = collections.Counter(stones)
    for _ in range(blinks):
        stone_count = next_stone_count(stone_count)
    return sum(stone_count.values())


solve_pt1 = functools.partial(solve, blinks=25)
solve_pt2 = functools.partial(solve, blinks=75)


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            stones = list(read_input(f))

        pt1 = solve_pt1(stones)
        print("Part 1:", pt1)

        pt2 = solve_pt2(stones)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
