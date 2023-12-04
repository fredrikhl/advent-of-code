"""
Advent of Code 2023

`Day 1 <https://adventofcode.com/2023/day/1>`_:
Trebuchet?!
"""
import functools
import os
import sys


def read_lines(fd):
    """ Read calorie counts from file-like. """
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        yield line


WORD_TO_DIGIT = {
    word: str(digit)
    for digit, word in enumerate((
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
    ), 1)}


def extract_digits(value, include_words):
    """ Get digits from *value* in order of appearance. """
    for i in range(len(value)):
        if value[i].isdigit():
            yield value[i]
            continue

        if not include_words:
            continue

        for word in WORD_TO_DIGIT:
            if value[i:].startswith(word):
                yield WORD_TO_DIGIT[word]
                break


def get_calibration_value(iterable):
    """ Combine the first and last value in iterable of digits to a number. """
    digits = list(iterable)
    if digits:
        return int("".join((digits[0], digits[-1])))
    # Not a valid calibration value.  E.g. solving the second example using
    # only part 1 rules.
    return 0


def solve(lines, include_words):
    """ Get sum of all valid calibration values from lines. """
    return sum(get_calibration_value(extract_digits(line, include_words))
               for line in lines)


solve_pt1 = functools.partial(solve, include_words=False)
solve_pt2 = functools.partial(solve, include_words=True)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            lines = list(read_lines(f))

        pt1 = solve_pt1(lines)
        print('Part 1:', pt1)

        pt2 = solve_pt2(lines)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
