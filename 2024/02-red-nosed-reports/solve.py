"""
Advent of Code 2024

`Day 2 <https://adventofcode.com/2024/day/2>`_:
Red-Nosed Reports
"""
import itertools
import os
import sys


def read_input(f):
    """ read number lists from file-like *f* """
    for lineno, raw_line in enumerate(f, 1):
        line = raw_line.strip()
        if not line:
            continue
        yield [int(p.strip()) for p in line.split()]


def check_report(levels):
    """ check if report *levels* are safe. """
    prevdir = 0
    for prev, curr in itertools.pairwise(levels):
        diff = curr - prev
        if abs(diff) > 3:
            return False
        currdir = (diff // abs(diff)) if diff else 0
        if not currdir:
            return False
        if prevdir and currdir != prevdir:
            return False
        prevdir = currdir
    return True


def solve_pt1(reports):
    """ count number of safe *reports* """
    return sum(check_report(report) for report in reports)


def problem_dampener(report):
    """ generate report candidates by removing a level """
    yield report
    for i in range(len(report)):
        yield report[:i] + report[i+1:]


def solve_pt2(reports):
    """ count number of safe *reports* when using the problem dampener """
    return sum(
        any(check_report(r) for r in problem_dampener(report))
        for report in reports
    )


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            data = list(read_input(f))

        pt1 = solve_pt1(data)
        print('Part 1:', pt1)

        pt2 = solve_pt2(data)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
