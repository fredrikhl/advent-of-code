""" Day 13: Shuttle Search """
import functools
import itertools
import operator
import os
import sys


def parse_file(fd):
    """ read instructins from a file-like object. """
    init = int(fd.readline())
    buses = tuple(None if v == 'x' else int(v)
                  for v in fd.readline().split(','))
    return init, buses


def get_wait(ts, busno):
    """ get remaining time until busno leaves. """
    return (busno - (ts % busno)) % busno


def find_first_available(buses, after):
    """ find first bus that leaves after a given time. """
    for ts in itertools.count(after):
        for busno in buses:
            if busno is not None and get_wait(ts, busno) == 0:
                return busno


def solve_next_bus(buses, after):
    """ Solve part 1: (busno * wait time) for the next available bus. """
    busno = find_first_available(buses, after)
    return get_wait(after, busno) * busno


def solve_contest(buses, max_ts=0):
    """ Solve part 2: Timestamp where wait time == offset for all buses. """
    in_service = tuple((offset, busno) for offset, busno
                       in enumerate(buses)
                       if busno is not None)

    ts = step = 1
    for offset, busno in in_service:
        for ts in itertools.count(ts, step):
            if get_wait(ts, busno) == offset % busno:
                step = step * busno
                break
    return ts


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main(inargs=None):
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        target, buses = tuple(parse_file(f))

    result = solve_next_bus(buses, target)
    print(f'Part 1: {result}')

    result = solve_contest(buses)
    print(f'Part 2: {result}')


if __name__ == '__main__':
    main()
