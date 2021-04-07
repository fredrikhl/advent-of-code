"""
AoC Day 6: Custom Customs
"""
import functools
import os
import sys


def read_groups(fd):
    """ read group answers from file-like object. """
    current = []
    for lineno, raw_line in enumerate(fd, 1):
        answers = set(raw_line.rstrip())
        if answers:
            current.append(answers)
        else:
            # end of current group - flush buffer
            yield tuple(current)
            current = []

    # eof - flush buffer
    if current:
        yield tuple(current)


def any_yes(group_answers):
    return functools.reduce(set.union, group_answers)


def all_yes(group_answers):
    return functools.reduce(set.intersection, group_answers)


def sum_groups(groups, aggregator):
    return sum(len(aggregator(group)) for group in groups)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        groups = tuple(read_groups(f))

    count = sum_groups(groups, any_yes)
    print(f'Part 1: {count}')

    count = sum_groups(groups, all_yes)
    print(f'Part 2: {count}')


if __name__ == '__main__':
    main()
