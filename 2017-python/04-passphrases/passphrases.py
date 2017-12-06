""" Advent of Code 2017

`Day 4 <http://adventofcode.com/2017/day/3>`_:
High-Entropy Passphrases
"""
from __future__ import print_function
import argparse
import collections


def has_no_duplicates(passphrase):
    words = passphrase.split()
    return len(words) == len(set(words))


def has_no_anagrams(passphrase):
    words = [''.join(sorted(word)) for word in passphrase.split()]
    return len(words) == len(set(words))


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'passwords',
        metavar='FILE',
        type=argparse.FileType('Ur'),
        help="file with passphrases, or '-' to read from STDIN")

    args = parser.parse_args(inargs)

    stats = collections.defaultdict(int)

    with args.passwords as f:
        for passphrase in f.readlines():
            if not passphrase.strip():
                continue
            stats['total'] += 1
            stats['no-duplicate'] += has_no_duplicates(passphrase)
            stats['no-anagram'] += has_no_anagrams(passphrase)

    print('Total:                 {total}'.format(**stats))
    print('Part 1, no duplicates: {no-duplicate}'.format(**stats))
    print('Part 2, no anagrams:   {no-anagram}'.format(**stats))


if __name__ == '__main__':
    main()
