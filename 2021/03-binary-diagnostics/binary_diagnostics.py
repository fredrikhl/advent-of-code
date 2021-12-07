""" Advent of Code 2021

`Day 3 <http://adventofcode.com/2021/day/3>`_:
Binary Diagnostic
"""
import operator
import os
import sys

MOST = operator.ge
LEAST = operator.lt


def parse_byte(value, bytesize=None):
    bits = tuple(int(b) for b in value.strip())
    if bytesize is not None and len(bits) != bytesize:
        raise ValueError("invalid bytesize %d (expected %d)"
                         % (len(bits), bytesize))
    if any(d > 1 or d < 0 for d in bits):
        raise ValueError('invalid digits')
    return bits


def read_bytes(fd):
    prev_len = None
    for lineno, line in enumerate(fd, 1):
        try:
            bits = parse_byte(line, bytesize=prev_len)
            yield bits
            prev_len = len(bits)
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def get_common(byte_tuples, cmp):
    limit = len(byte_tuples) / 2
    count = [0] * len(byte_tuples[0])
    for byte in byte_tuples:
        for i, d in enumerate(byte):
            count[i] += d
    return tuple(cmp(v, limit) for v in count)


def match_bytes(byte_tuples, pos, val):
    return tuple(byte for byte in byte_tuples
                 if byte[pos] == val)


def reduce_common(byte_tuples, cmp):
    size = len(byte_tuples[0])
    for bitpos in range(size):
        common = get_common(byte_tuples, cmp)[bitpos]
        byte_tuples = match_bytes(byte_tuples, bitpos, common)
        if len(byte_tuples) == 1:
            break

    return byte_tuples[0]


def to_number(byte):
    return sum(
        bit * 2 ** exp
        for exp, bit in enumerate(reversed(byte)))


def solve_pt1(byte_tuples):
    gamma = get_common(byte_tuples, MOST)
    epsilon = get_common(byte_tuples, LEAST)
    return to_number(gamma) * to_number(epsilon)


def solve_pt2(byte_tuples):
    oxygen = reduce_common(byte_tuples, MOST)
    co2 = reduce_common(byte_tuples, LEAST)
    return to_number(oxygen) * to_number(co2)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            byte_tuples = tuple(read_bytes(f))

        pt1 = solve_pt1(byte_tuples)
        print('Part 1:', pt1)
        pt2 = solve_pt2(byte_tuples)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
