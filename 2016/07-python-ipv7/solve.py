#!/usr/bin/env python3
"""
Advent of Code 2016

Day 7: Internet Protocol Version 7
"""
import os
import sys


def read_file(filename):
    with open(filename) as f:
        for lineno, line in enumerate(f, 1):
            line = line.rstrip()
            if not line:
                continue
            yield lineno, line.rstrip()


def sliding_bracket_window(value, size):
    """
    A sliding window that keeps track of open/close brackets.

    - Brackets cannot be nested: [[]]
    - Window resets on bracket open/bracket close: []
    - Only returns full windows
    """
    buffer = ''
    in_brackets = False
    for charno, char in enumerate(value, 1):
        if char == '[':
            if in_brackets:
                # Syntax error: open bracket inside brackets
                raise ValueError('nested brackets in pos %d: %s'
                                 % (charno, repr(value)))
            else:
                in_brackets = True
                buffer = ''
            continue
        if char == ']':
            if in_brackets:
                in_brackets = False
                buffer = ''
            else:
                # Syntax error: closing bracket outside brackets
                raise ValueError('unexpected bracket in pos %d: %s'
                                 % (charno, repr(value)))
            continue

        buffer += char
        if len(buffer) < size:
            continue

        if len(buffer) > size:
            buffer = buffer[-size:]

        yield in_brackets, buffer

    if in_brackets:
        # Syntax error: unclosed bracket
        raise ValueError('missing bracket in pos %d: %s'
                         % (charno, repr(value)))


def is_abba(value):
    """ if value matches the ABBA pattern. """
    return (len(value) == 4
            and value[0] == value[3]
            and value[1] == value[2]
            and value[0] != value[1])


def is_tls(value):
    """ if value matches the TLS requirements. """
    has_abba = False
    for is_hypernet, chars in sliding_bracket_window(value, 4):
        if not is_abba(chars):
            # not abba - don't know yet
            continue
        if is_hypernet:
            # abba in hypernet - *not* tls
            return False
        # abba in supernet - *maybe* tls, but must check for abba in hypernet
        has_abba = True
    return has_abba


def is_triplet(value):
    """ if value matches the ABA pattern. """
    return (len(value) == 3
            and value[0] == value[2]
            and value[0] != value[1])


def invert_triplet(value):
    """ convert BAB -> ABA -> BAB. """
    if is_triplet(value):
        return "".join((value[1], value[0], value[1]))
    raise ValueError('invalid triplet: ' + repr(value))


def is_ssl(value):
    """ if value matches the SSL requirements. """
    aba_supernets = set()
    aba_hypernets = set()

    # first pass - sort all triplets into supernet and hypernet sets
    for is_hypernet, chars in sliding_bracket_window(value, 3):
        if not is_triplet(chars):
            continue
        if is_hypernet:
            aba_hypernets.add(invert_triplet(chars))
        else:
            aba_supernets.add(chars)
    return any(aba in aba_hypernets for aba in aba_supernets)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        lines = tuple(line for lineno, line in read_file(filename))

        print("Part 1:", sum(is_tls(v) for v in lines))
        print("Part 2:", sum(is_ssl(v) for v in lines))


if __name__ == "__main__":
    main()
