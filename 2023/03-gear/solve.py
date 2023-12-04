"""
Advent of Code 2023

`Day 3 <https://adventofcode.com/2023/day/3>`_:
Gear Ratios
"""
import operator
import os
import sys


def read_schematic(fd):
    """ Read position and value from file-like *fd*. """
    rownum = 0
    for lineno, line in enumerate(fd, 1):
        if not line.strip():
            continue
        try:
            row = tuple(line.strip())
            for colnum, char in enumerate(row):
                if char == ".":
                    # ignore "empty values" (not a digit, not a part)
                    continue
                yield (rownum, colnum), char
            rownum += 1
        except Exception as e:
            raise ValueError('invalid input on line %d (%r): %s' %
                             (lineno, line, e))


def find_number_start(matrix, curr):
    """ Get number start position for a digit in position *curr*. """
    if curr not in matrix or not matrix[curr].isdigit():
        raise ValueError("not a digit: %r @ %r" % (matrix.get(curr), curr))
    # move left until we run out of digits
    left = (curr[0], curr[1] - 1)
    while left in matrix and matrix[left].isdigit():
        curr, left = left, (left[0], left[1] - 1)
    return curr


def get_number_at(matrix, curr):
    """ Get number value from digits starting at position *curr*. """
    if curr not in matrix or not matrix[curr].isdigit():
        raise ValueError("not a digit: %r @ %r" % (matrix.get(curr), curr))
    digits = []
    # get digit at *curr* and move right
    while curr in matrix and matrix[curr].isdigit():
        digits.append(matrix[curr])
        curr = (curr[0], curr[1] + 1)
    return int("".join(digits))


NEIGHBOR_DELTAS = (
    (-1, -1), (-1, +0), (-1, +1),
    (+0, -1), (+0, +1),
    (+1, -1), (+1, +0), (+1, +1),
)


def get_parts(matrix):
    """ Get a mapping of part position to neighboring part numbers. """
    # collect some position lookup tables:
    # - digit position to number start position
    # - part positions to part number start positions (empty, for now)
    number_start_pos = {}
    part_number_pos = {}
    for point in matrix:
        if matrix[point].isdigit():
            number_start_pos[point] = find_number_start(matrix, point)
        else:
            part_number_pos[point] = set()

    # fill in part number start positions
    for point in part_number_pos:
        for delta in NEIGHBOR_DELTAS:
            neighbor = (point[0] + delta[0], point[1] + delta[1])
            if neighbor in matrix and neighbor in number_start_pos:
                part_number_pos[point].add(number_start_pos[neighbor])

    # get actual number value at each number start position
    numbers = {}
    for start_pos in set(number_start_pos.values()):
        numbers[start_pos] = get_number_at(matrix, start_pos)

    # map part position -> list of neighboring part numbers
    return {part_pos: [numbers[number_pos]
                       for number_pos in part_number_pos[part_pos]]
            for part_pos in part_number_pos}


def solve_pt1(matrix):
    parts = get_parts(matrix)
    return sum(value for values in parts.values() for value in values)


def find_value(matrix, value):
    """ Find positions with a given value. """
    for point in matrix:
        if matrix[point] == value:
            yield point


def solve_pt2(matrix):
    parts = get_parts(matrix)
    ratios = []
    for gear_pos in find_value(matrix, "*"):
        part_numbers = parts.get(gear_pos) or []
        if len(part_numbers) == 2:
            ratios.append(operator.mul(*part_numbers))
    return sum(ratios)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            schematic = dict(read_schematic(f))

        pt1 = solve_pt1(schematic)
        print('Part 1:', pt1)

        pt2 = solve_pt2(schematic)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
