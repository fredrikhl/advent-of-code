"""
AoC Day 3: Toboggan Trajectory
"""
import collections
import functools
import io
import operator
import os
import sys


SQUARE, TREE = CHARS = '.#'


def parse_row(text):
    for pos, char in enumerate(text, 1):
        if char in CHARS:
            yield char
        else:
            raise ValueError('invalid char in col %d: %r' % (pos, char))


def read_rows(fd):
    """ read and parse area structure from a file-like object. """
    prev_cols = None
    for lineno, line in enumerate(fd, 1):
        try:
            row = tuple(parse_row(line.strip()))
            if prev_cols is not None and len(row) != prev_cols:
                raise ValueError('invalid row length %d, expected %d' %
                                 (len(row), prev_cols))
            yield row
            prev_cols = len(row)
        except Exception as e:
            raise ValueError('error on line %d (%r): %s' % (lineno, line, e))


def move(matrix, current, delta):
    """ Calculate a new position in the matrix. """
    col, row = current
    col_shift, row_shift = delta
    ncols = len(matrix[0])
    return (
        (col + col_shift) % ncols,
        (row + row_shift),
    )


def generate_path(matrix, start, delta):
    """ Generate positions by following a movement pattern (delta). """
    col, row = start
    while row < len(matrix):
        yield col, row
        col, row = move(matrix, (col, row), delta)


def is_tree(forest, position):
    """ Check if position in matrix is a tree. """
    col, row = position
    return forest[row][col] == TREE


def count_trees(forest, slope):
    path = generate_path(forest, (0, 0), slope)
    return sum(is_tree(forest, p) for p in path)


def solve_product(forest, slopes):
    tree_counts = (count_trees(forest, t) for t in slopes)
    return functools.reduce(operator.mul, tree_counts, 1)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        forest = tuple(read_rows(f))

    trees = count_trees(forest, (3, 1))
    print(f'Part 1: {trees}')

    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    product = solve_product(forest, slopes)
    print(f'Part 2: {product}')


if __name__ == '__main__':
    main()
