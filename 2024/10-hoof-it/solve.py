"""
Advent of Code 2024

`Day 10 <https://adventofcode.com/2024/day/10>`_
Hoof It
"""
import os
import sys

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
MIN_HEIGHT = 0
MAX_HEIGHT = 9


def read_map(f):
    """ read position and height pairs from file-like *f*. """
    rownum = 0
    for lineno, raw_line in enumerate(f, 1):
        line = raw_line.strip()
        if not line:
            continue
        for colnum, char in enumerate(line):
            if char == ".":
                continue  # example file support
            try:
                yield ((rownum, colnum), int(char))
            except ValueError:
                raise ValueError("invalid input on line %d (%r): %r"
                                 % (lineno, raw_line, char))
        rownum += 1


def find_trailheads(topography):
    """ find all trailheads in a given *topography*. """
    heads = set(p for p in topography if topography[p] == MIN_HEIGHT)
    if not heads:
        raise RuntimeError("no trailheads in topography")
    return heads


def get_valid_steps(topography, currpos):
    """ find valid next steps from *currpos* in *topography* """
    next_height = topography[currpos] + 1
    neighbors = ((currpos[0] + d[0], currpos[1] + d[1]) for d in DIRECTIONS)
    return (n for n in neighbors if topography.get(n, -1) == next_height)


def find_paths(topography, path):
    """ find all paths in *topography* that leads to a *MAX_HEIGHT*. """
    currpos = path[-1]
    if topography[currpos] == MAX_HEIGHT:
        yield path
    else:
        for nextpos in get_valid_steps(topography, currpos):
            yield from find_paths(topography, path + (nextpos,))


def solve_pt1(topography):
    """ find the sum of all trail scores in *topography* """
    return sum(
        len(set(path[-1] for path in find_paths(topography, (trailhead,))))
        for trailhead in find_trailheads(topography)
    )


def solve_pt2(topography):
    """ find the sum of all trail ratings in *topography* """
    return sum(
        1
        for trailhead in find_trailheads(topography)
        for _ in find_paths(topography, (trailhead,))
    )


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            topography = dict(read_map(f))

        pt1 = solve_pt1(topography)
        print("Part 1:", pt1)

        pt2 = solve_pt2(topography)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
