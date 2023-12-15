"""
Advent of Code 2023

`Day 6 <https://adventofcode.com/2023/day/2>`_:
Wait For It
"""
import functools
import operator
import os
import re
import sys


RE_TIME = re.compile(r"Time:\s+(.*)")
RE_DIST = re.compile(r"Distance:\s+(.*)")
RE_NUMS = re.compile(r"\d+")


def read_records(fd):
    """ Read time and distance lists from file-like *fd*. """
    times = []
    distances = []
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            for regex, results in ((RE_TIME, times), (RE_DIST, distances)):
                if (m := regex.match(line)):
                    results.extend(int(n) for n in RE_NUMS.findall(m.group(1)))
                    continue
        except Exception as e:
            raise ValueError("Invalid value on line %d: %s (%s)"
                             % (lineno, repr(line), e))

    if not times:
        raise ValueError("No time values")
    if not distances:
        raise ValueError("No distance values")
    if len(times) != len(distances):
        raise ValueError("Unbalanced number of values (%d times, %d distances)"
                         % (len(times), len(distances)))

    return times, distances


def get_distance(hold_time, total_time):
    speed = hold_time
    move_time = total_time - hold_time
    return move_time * speed


def find_lowest_win(time, distance):
    """ Find the lowest time that can beat the distance. """
    curr = 1
    while (curr < time):
        if get_distance(curr, time) > distance:
            return curr
        curr += 1
    raise RuntimeError("impossible to beat %d mm in %d ms"
                       % (distance, time))


def find_highest_win(time, distance):
    """ Find the highest time that can beat the distance. """
    curr = time - 1
    while (0 < curr):
        if get_distance(curr, time) > distance:
            return curr
        curr -= 1
    raise RuntimeError("impossible to beat %d mm in %d ms"
                       % (distance, time))


def find_win_range(time, distance):
    """
    Find start and stop arguments for generating a winning range.

    Note: As with the *range* builtin, stop is not inclusive.
    """
    # There is probably some algorithm to find these intersection points faster.
    # Maybe a binary search and use the slope to neighboring points to figure
    # out in which half the high/low point is?
    return (find_lowest_win(time, distance),
            find_highest_win(time, distance) + 1)


def solve(times, distances):
    range_sizes = []
    for time, distance in zip(times, distances):
        start, stop = find_win_range(time, distance)
        range_sizes.append(stop - start)
    return functools.reduce(operator.mul, range_sizes, 1)


def solve_pt1(records):
    times, distances = records
    return solve(times, distances)


def combine_digits(digits):
    return int("".join(str(n) for n in digits))


def solve_pt2(records):
    times, distances = records
    times = [combine_digits(times)]
    distances = [combine_digits(distances)]
    return solve(times, distances)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            records = list(read_records(f))

        pt1 = solve_pt1(records)
        print('Part 1:', pt1)

        pt2 = solve_pt2(records)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
