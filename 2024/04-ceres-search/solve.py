"""
Advent of Code 2024

`Day 4 <https://adventofcode.com/2024/day/4>`_:
Ceres Search
"""
import os
import sys


DIRECTIONS = {
    'NW': (-1, -1), 'N': (-1, 0), 'NE': (-1, 1),
    'W': (0, -1), 'E': (0, 1),
    'SW': (1, -1), 'S': (1, 0), 'SE': (1, 1),
}


def read_map(f):
    """ read position and letter pairs from file-like *f*. """
    rownum = 0
    for lineno, line in enumerate(f, 1):
        if not line.strip():
            continue
        try:
            for colnum, char in enumerate(line.strip()):
                yield (rownum, colnum), char
            rownum += 1
        except Exception as e:
            raise ValueError('invalid input on line %d (%r): %s' %
                             (lineno, line, e))


def is_word(lettermap, start, direction, word):
    """ check if *word* is present at a *start* in *lettermap*. """
    row, col = start
    row_d, col_d = direction
    vector = ((row + row_d * i, col + col_d * i) for i in range(len(word)))
    return "".join(lettermap.get(p, "") for p in vector) == word


def count_words(lettermap, point, word):
    return sum(
        is_word(lettermap, point, d, word)
        for d in DIRECTIONS.values()
    )


def solve_pt1(lettermap):
    # optimize: only consider points starting with "X":
    candidates = set(p for p in lettermap if lettermap[p] == "X")
    return sum(count_words(lettermap, point, "XMAS") for point in candidates)


def count_cross_words(lettermap, point, word):
    """ find number of diagonal *word* in *lettermap* meeting at *point*. """
    row, col = point
    half = len(word) // 2
    directions = [DIRECTIONS[d] for d in ("SE", "NE", "SW", "NW")]
    starting_points = (
        (row - row_d * half, col - col_d * half)
        for row_d, col_d in directions
    )
    return sum(
        is_word(lettermap, p, d, word)
        for p, d in zip(starting_points, directions)
    )


def solve_pt2(lettermap):
    # optimize: only consider points meeting at an "A":
    candidates = set(p for p in lettermap if lettermap[p] == "A")
    return sum(count_cross_words(lettermap, p, "MAS") == 2 for p in candidates)


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            data = dict(read_map(f))

        pt1 = solve_pt1(data)
        print("Part 1:", pt1)

        pt2 = solve_pt2(data)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
