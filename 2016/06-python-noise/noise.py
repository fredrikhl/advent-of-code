#!/usr/bin/env python3
"""
Advent of Code 2016

Day 6: Signals and Noise
"""
import collections
import itertools
import os
import sys


def read_file(filename):
    line_length = None
    with open(filename) as f:
        for lineno, line in enumerate(f, 1):
            line = line.rstrip()
            if not line:
                continue
            if line_length is None:
                line_length = len(line)
            elif len(line) != line_length:
                raise ValueError(
                    "invalid length on line %d (expected %d): %s"
                    % (len(line), line_length, repr(line)))
            yield lineno, line.rstrip()


def flip(lines):
    lines = tuple(lines)
    length = len(lines[0])
    for i in range(length):
        yield "".join(line[i] for line in lines)


def get_char(string, most_common=True):
    """ generate checksum for a given (encrypted) name. """
    char_counts = collections.Counter(string)
    sort_factor = -1 if most_common else 1
    ordered = sorted(char_counts.items(),
                     key=lambda t: (sort_factor * t[1], t[0]))
    return ''.join(char for char, _ in itertools.islice(ordered, 1))


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        lines = (line for lineno, line in read_file(filename))

        part_1 = []
        part_2 = []
        for chars in flip(lines):
            part_1.append(get_char(chars, True))
            part_2.append(get_char(chars, False))
        print("Part 1:", "".join(part_1))
        print("Part 2:", "".join(part_2))


if __name__ == "__main__":
    main()
