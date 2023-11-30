#!/usr/bin/env python3
"""
Advent of Code 2016

Day 4: Security Through Obscurity
"""
import argparse
import collections
import itertools
import logging
import re
import sys
import string

logger = logging.getLogger(__name__)

LOG_FORMAT = '%(levelname)s: %(message)s'

# regex for parsing input lines (room-ids)
ROOM_REGEX = re.compile(r"(?P<name>[-a-z]+)-(?P<sid>\d+)\[(?P<chk>[a-z]+)\]")

# Search terms for finding the room with North Pole objects
SEARCH_TERMS = ('north', 'pole', 'object')


def parse_room_id(value):
    """ parse room-id into (encrypted-name, sector-id, checksum). """
    mg = ROOM_REGEX.match(value)
    if mg:
        return mg.group('name'), int(mg.group('sid')), mg.group('chk')
    raise ValueError("invalid room id: " + repr(value))


def read_room_file(iterable):
    """ parse lines from an iterable or file-like object """
    for lineno, raw_line in enumerate(iterable, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            yield parse_room_id(line)
        except Exception as e:
            raise ValueError("invalid room id on line %d: %r (%r)"
                             % (lineno, raw_line, e))


def read_rooms(filename):
    """ iterate over lines from file (or stdin). """
    if filename == '-':
        yield from read_room_file(sys.stdin)
        return
    with open(filename) as f:
        yield from read_room_file(f)


def checksum(string):
    """ generate checksum for a given (encrypted) name. """
    char_counts = collections.Counter(string.replace('-', ''))
    # Counter.most_common(5) won't solve tie-breaks, and sorted(reversed=True)
    # will also reverse our tie-breaks:
    most_common = sorted(char_counts.items(), key=lambda t: (-t[1], t[0]))
    return ''.join(char for char, _ in itertools.islice(most_common, 5))


def decrypt(encrypted, sector):
    """ decrypt room name. """
    from_tr = string.ascii_lowercase + '-'
    s = collections.deque(list(string.ascii_lowercase))
    s.rotate(-(sector % len(string.ascii_lowercase)))
    to_tr = ''.join(s) + ' '
    return encrypted.translate(str.maketrans(from_tr, to_tr))


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose',
        action='store_const',
        dest='log_level',
        const=logging.DEBUG,
        default=logging.ERROR,
        help="more verbose logging",
    )
    parser.add_argument(
        'input',
        metavar='FILE',
        help="file with digits to read, or '-' to read from STDIN",
    )
    args = parser.parse_args(inargs)
    logging.basicConfig(format=LOG_FORMAT, level=args.log_level)

    pt1_sum = 0
    pt2_candidates = []

    for enc, sid, chk in read_rooms(args.input):
        if checksum(enc) != chk:
            continue
        pt1_sum += sid
        name = decrypt(enc, sid)
        if all(word in name for word in SEARCH_TERMS):
            logger.info("room candidate: sid=%r, name=%r", sid, name)
            pt2_candidates.append(sid)

    print('Part 1:', pt1_sum)
    print('Part 2:', ', '.join(str(s) for s in pt2_candidates))


if __name__ == '__main__':
    main()
