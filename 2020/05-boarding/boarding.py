"""
AoC Day 5: Binary Boarding
"""
import re
import os
import sys

ROWS = 128
COLS = 8

BSP_RE = re.compile('[FB]{7}[LR]{3}')
BSP_TR = str.maketrans('FBLR', '0101')


def read_bsp(fd):
    """ read seat instructions from file. """
    for lineno, line in enumerate(fd, 1):
        try:
            yield BSP_RE.fullmatch(line.rstrip()).group(0)
        except AttributeError:
            raise ValueError('invalid bsp on line %d (%r)' % (lineno, line))


def get_seat(seat_id):
    """ get seat row and column from seat id. """
    return seat_id // COLS, seat_id % COLS


def get_seat_id(bspstr):
    """ parse seat instructions into a seat id. """
    return int(bspstr.translate(BSP_TR), 2)


def find_vacant_seats(seat_ids):
    """ finds vacant seats, given no two vacant seat ids are adjacent. """
    return (i for i in set(range(ROWS * COLS)) - seat_ids
            if all(n in seat_ids for n in (i + 1, i - 1)))


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        seat_ids = set(get_seat_id(b) for b in read_bsp(f))

    highest_id = max(seat_ids)
    highest_seat = get_seat(highest_id)
    print(f'Part 1: {highest_id} {highest_seat}')

    vacant_id = next(find_vacant_seats(seat_ids))
    vacant_seat = get_seat(vacant_id)
    print(f'Part 2: {vacant_id} {vacant_seat}')


if __name__ == '__main__':
    main()
