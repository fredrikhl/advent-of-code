"""
AoC Day 2: Password Philosophy
"""
import collections
import io
import os
import re
import sys


entry_t = collections.namedtuple('Entry', ('a', 'b', 'char', 'passwd'))
entry_regex = re.compile(r'^(\d+)-(\d+) (.): (.*)$')
entry_types = (int, int, str, str)


def parse_entry(text):
    m_res = entry_regex.match(text)
    return entry_t(*(t(v) for t, v in zip(entry_types, m_res.groups())))


def read_entries(fd):
    """ read and parse password entries from a file-like object. """
    for lineno, line in enumerate(fd, 1):
        try:
            yield parse_entry(line.strip())
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def is_valid_count(entry):
    """ check if entry is valid according to part 1. """
    return entry.a <= collections.Counter(entry.passwd)[entry.char] <= entry.b


def is_valid_pos(entry):
    """ check if entry is valid according to part 2. """
    pos_match = [entry.char == entry.passwd[p]
                 for p in (entry.a - 1, entry.b - 1)]
    return any(pos_match) and not all(pos_match)


def count_valid(entries, is_valid):
    """ Count number of valid entries accoring to callback. """
    return len(tuple(filter(is_valid, entries)))


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        entries = tuple(read_entries(f))

    result = count_valid(entries, is_valid_count)
    print(f'Part 1: {result}')

    result = count_valid(entries, is_valid_pos)
    print(f'Part 2: {result}')


if __name__ == '__main__':
    main()
