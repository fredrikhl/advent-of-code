""" Advent of Code 2022

`Day 9 <https://adventofcode.com/2022/day/9>`_:
Rope Bridge
"""
import functools
import os
import sys


# Delta for each direction
DIRECTION_MAP = {
    "U":  (0,  1),
    "D":  (0, -1),
    "R":  (1,  0),
    "L": (-1,  0),
}


def read_input(fd):
    """ Read and parse input from file. """
    for lineno, raw_line in enumerate(fd, 1):
        if not (line := raw_line.strip()):
            continue
        try:
            direction, steps = line.split(" ", 1)
            yield (DIRECTION_MAP[direction], int(steps))
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def tail_step(current, target):
    """ Get next step (delta) towards *target*. """
    diff = (target[0] - current[0], target[1] - current[1])
    if max(abs(i) for i in diff) <= 1:
        # We're already at target, or at a neighbor of target
        return None

    return tuple((i // abs(i)) if i else 0 for i in diff)


def add_delta(position, delta):
    return (position[0] + delta[0], position[1] + delta[1])


def follow_steps(steps, current=(0, 0)):
    """ Follow movements of a rope head. """
    yield current
    for target in steps:
        while s := tail_step(current, target):
            current = add_delta(current, s)
            yield current


def generate_steps(instructions, current=(0, 0)):
    """ Generate positions from instructions. """
    yield current
    for delta, n in instructions:
        for _ in range(n):
            current = add_delta(current, delta)
            yield current


def solve(instructions, tails):
    steps = generate_steps(instructions)

    for _ in range(tails):
        steps = follow_steps(steps)

    return len(set(steps))


solve_pt1 = functools.partial(solve, tails=1)
solve_pt2 = functools.partial(solve, tails=9)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = tuple(read_input(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
