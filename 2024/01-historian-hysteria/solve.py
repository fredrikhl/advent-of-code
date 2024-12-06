"""
Advent of Code 2024

`Day 1 <https://adventofcode.com/2024/day/1>`_:
Historian Hysteria
"""
import os
import sys


def read_input(f):
    """ read columns of number pairs from file-like *f* """
    columns = ([], [])
    for lineno, raw_line in enumerate(f, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            row = (int(p.strip()) for p in line.split())
            for col, val in zip(columns, row):
                col.append(val)
        except Exception as e:
            raise ValueError('invalid input on line %d (%r): %s' %
                             (lineno, line, e))
    return columns


def solve_pt1(columns):
    col_a, col_b = [sorted(c) for c in columns]
    return sum(abs(a - b) for a, b in zip(col_a, col_b))


def get_similarity_lut(column):
    """ get a similarity lookup table for a column. """
    lut = {}
    for location_id in column:
        if location_id in lut:
            lut[location_id] += 1
        else:
            lut[location_id] = 1
    return lut


def solve_pt2(columns):
    col_a, col_b = columns
    similarity = get_similarity_lut(col_b)
    return sum(
        similarity.get(location_id, 0) * location_id
        for location_id in col_a
    )


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            columns = list(read_input(f))

        pt1 = solve_pt1(columns)
        print('Part 1:', pt1)

        pt2 = solve_pt2(columns)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
