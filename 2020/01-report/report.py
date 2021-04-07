""" Advent of Code 2020

`Day 1 <http://adventofcode.com/2020/day/1>`_:
Report Repair
"""
import functools
import itertools
import operator
import os
import sys


TARGET_SUM = 2020


def read_numbers(fd):
    """ Read numbers from a file-like object. """
    for lineno, line in enumerate(fd, 1):
        try:
            yield int(line)
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def mul(*args):
    return functools.reduce(operator.mul, args, 1)


def find_combo(numbers, target_sum, n):
    for combo in itertools.combinations(numbers, n):
        if sum(combo) == target_sum:
            return combo

    raise ValueError('no valid numbers')


def solve(numbers, target_sum, n):
    combo = find_combo(numbers, target_sum, n)
    return combo, mul(*combo)


def format_solution(solution_t):
    combo, product = solution_t
    return '{} = {}'.format(' * '.join(str(c) for c in combo), product)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        numbers = tuple(read_numbers(f))

    res = solve(numbers, TARGET_SUM, 2)
    print("Part 1:", format_solution(res))

    res = solve(numbers, TARGET_SUM, 3)
    print("Part 2:", format_solution(res))


if __name__ == '__main__':
    main()
