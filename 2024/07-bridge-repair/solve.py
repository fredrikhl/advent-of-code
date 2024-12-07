"""
Advent of Code 2024

`Day 7 <https://adventofcode.com/2024/day/7>`_:
Bridge Repair
"""
import itertools
import operator
import os
import sys


def read_items(f):
    """ read result and operand pairs from a file-like *f*. """
    for lineno, line in enumerate(f, 1):
        if not line.strip():
            continue
        try:
            result, rest = line.split(": ", 1)
            yield (
                int(result),
                tuple(int(a) for a in rest.split(" ")),
            )
        except Exception as e:
            raise ValueError("invalid input on line %d (%r): %s"
                             % (lineno, line, e))


def apply_operators(operators, operands):
    """ apply a sequence of N-1 operators to a sequence of N numbers. """
    total = operands[0]
    for fn, value in zip(operators, operands[1:]):
        total = fn(total, value)
    return total


class Solver(object):
    """ a set of *operators* to apply to *operands* to get *answer*. """

    def __init__(self, *operators):
        self.operators = operators

    def __call__(self, operands, answer):
        """ check if a solution exists for the *operands* and *answer* """
        n = len(operands) - 1
        return any(apply_operators(combo, operands) == answer
                   for combo in itertools.product(self.operators, repeat=n))


def solve_pt1(data):
    is_solvable = Solver(operator.add, operator.mul)
    return sum(
        answer
        for answer, operands in data
        if is_solvable(operands, answer)
    )


def concatenate(a, b):
    """ concatenate the digits of two integers, *a* and *b*. """
    return a * (10 ** len(str(b))) + b


def solve_pt2(data):
    is_solvable = Solver(operator.add, operator.mul, concatenate)
    return sum(
        answer
        for answer, operands in data
        if is_solvable(operands, answer)
    )


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            data = list(read_items(f))

        pt1 = solve_pt1(data)
        print("Part 1:", pt1)

        pt2 = solve_pt2(data)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
