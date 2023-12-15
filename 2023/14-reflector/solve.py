"""
Advent of Code 2023

`Day 14 <https://adventofcode.com/2023/day/14>`_:
Parabolic Reflector Dish
"""
import functools
import os
import sys

ROUND = "O"
SPACE = "."


# Direction to next position transformers
MOVE = {
    "N": lambda t: (t[0] - 1, t[1]),
    "W": lambda t: (t[0], t[1] - 1),
    "S": lambda t: (t[0] + 1, t[1]),
    "E": lambda t: (t[0], t[1] + 1),
}


# Spin sequence
SPIN = ("N", "W", "S", "E")


# Direction to sorting functions.  These sorters decide which order each rock
# should be processed in.  E.g. when shifting rocks towards the north, we start
# with entries closest to the north edge (lowest row first) so they can land
# before we process later rocks.
SHIFT_ORDER = {
    "N": sorted,
    "W": functools.partial(sorted, key=lambda t: (t[1], t[0])),
    "S": functools.partial(sorted, reverse=True),
    "E": functools.partial(sorted, key=lambda t: (-t[1], t[0])),
}


def read_matrix(fd):
    """ Read position and value from file-like *fd*. """
    rownum = 0
    for lineno, line in enumerate(fd, 1):
        if not line.strip():
            continue
        try:
            row = tuple(line.strip())
            for colnum, char in enumerate(row):
                yield (rownum, colnum), char
            rownum += 1
        except Exception as e:
            raise ValueError('invalid input on line %d (%r): %s' %
                             (lineno, line, e))


def get_movable(matrix, direction="N"):
    """ Get all movable rocks, sorted by the order they should move in. """
    sort = SHIFT_ORDER[direction]
    return sort(pos for pos, char in matrix.items() if char == ROUND)


def shift(matrix, direction):
    """ Move all movable rocks in a given direction until they can't move. """
    move = MOVE[direction]
    for pos in get_movable(matrix, direction):
        while True:
            next_pos = move(pos)
            if matrix.get(next_pos) != SPACE:
                # We've hit something, and can't "fall" any further
                break
            matrix[pos], matrix[next_pos] = SPACE, matrix[pos]
            pos = next_pos


def calculate_load(matrix):
    """ Calculate the tital load. """
    max_weight = max(row for row, _ in matrix) + 1
    return sum(max_weight - row for row, _ in get_movable(matrix))


def solve_pt1(values):
    matrix = dict(values)
    shift(matrix, "N")
    return calculate_load(matrix)


def get_fingerprint(matrix):
    """ Get a signature to identify a given matrix layout. """
    return "".join(repr(p) for p in get_movable(matrix))


def spin(matrix, n):
    """ Perform a spin on the matrix *n* times. """
    cycle_detection = {}
    i = 0
    while i < n:
        fp = get_fingerprint(matrix)
        if fp in cycle_detection:
            # We've found a cycle - let's skip ahead
            cycle_size = i - cycle_detection[fp]
            cycles_remaining = (n - i) // cycle_size
            i += cycles_remaining * cycle_size
        cycle_detection[fp] = i
        for direction in SPIN:
            shift(matrix, direction)
        i += 1


def solve_pt2(values):
    matrix = dict(values)
    spin(matrix, 1_000_000_000)
    return calculate_load(matrix)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = dict(read_matrix(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
