""" Day 11: Seating System """
import os
import sys


FLOOR, EMPTY, TAKEN = CHARS = '.L#'

DIRECTIONS = (
    (0, -1),   # N
    (1, -1),   # NE
    (1, 0),    # E
    (1, 1),    # SE
    (0, 1),    # S
    (-1, 1),   # SW
    (-1, 0),   # W
    (-1, -1),  # NW
)


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


def iter_matrix(matrix):
    """ Iterate over all possible positions. """
    for rownum, row in enumerate(matrix):
        for colnum, col in enumerate(row):
            yield (colnum, rownum), col


def count_seats(matrix, seat):
    """ Count number of seats in matrix. """
    return len([value for _, value in iter_matrix(matrix) if value == seat])


def get_kernel(matrix, current, limit):
    """ Get relevant seats for the current position. """
    def walk(delta):
        col_shift, row_shift = delta
        col, row = current
        count = 0
        while True:
            prev = col, row
            col, row = col + col_shift, row + row_shift
            count += 1
            if col < 0 or row < 0:
                # out of bounds (N, W)
                return prev
            try:
                if matrix[row][col] != FLOOR:
                    # found visible
                    return col, row
            except IndexError:
                # out of bounds (S, E)
                return prev

            if limit and count >= limit:
                # <limit> steps reached
                return col, row

    return set(walk(d) for d in DIRECTIONS) - set((current,))


def next_value(matrix, position, visible):
    """ Get next value for a given position. """
    currval = matrix[position[1]][position[0]]
    if currval == FLOOR:
        return currval
    taken_limit = 4 + bool(visible)
    kernel_limit = not visible
    num_taken = sum(matrix[row][col] == TAKEN
                    for col, row in get_kernel(matrix, position, kernel_limit))
    if currval == EMPTY and num_taken < 1:
        return TAKEN
    if currval == TAKEN and num_taken >= taken_limit:
        return EMPTY
    return currval


def get_changes(matrix, visible):
    """ get all position changes in next shift. """
    for position, value in iter_matrix(matrix):
        newval = next_value(matrix, position, visible)
        if newval != value:
            yield position + (newval,)


def solve(matrix, visible):
    """ shift positions until equilibrium is reached. """
    current = list(list(r) for r in matrix)  # mutable
    while True:
        changes = tuple(get_changes(current, visible))
        if not changes:
            break
        for col, row, val in changes:
            current[row][col] = val
    return tuple(tuple(r) for r in current)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main(inargs=None):
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        matrix = tuple(read_rows(f))

    taken = count_seats(solve(matrix, visible=False), TAKEN)
    print(f"Part 1: {taken}")

    taken = count_seats(solve(matrix, visible=True), TAKEN)
    print(f"Part 2: {taken}")


if __name__ == '__main__':
    main()
