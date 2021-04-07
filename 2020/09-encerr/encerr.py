import itertools
import os
import sys


def read_numbers(fd):
    """ read numbers from a file-like object. """
    for lineno, line in enumerate(fd, 1):
        try:
            yield int(line.rstrip())
        except Exception as e:
            raise ValueError('error on line %d (%r): %s' % (lineno, line, e))


def iter_contiguous(sequence, size, offset=1):
    """ get all sequences of length *n* in *sequence*.

    >>> list(iter_contiguous((1, 2, 3, 4, 5), 3))
    [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    """
    start, end = 0, size
    while end <= len(sequence):
        yield sequence[start:end]
        start, end = start + offset, end + offset


def get_valid(preamble):
    """ get all valid numbers for a given preamble. """
    pairs = itertools.combinations(preamble, 2)
    return set(map(sum, pairs))


def get_invalid_values(numbers, preamble_size):
    """ get invalid numbers in a given number sequence. """
    for t in iter_contiguous(numbers, preamble_size + 1):
        preamble, num = t[:-1], t[-1]
        if num not in get_valid(preamble):
            yield num


def find_range(numbers, target_value):
    """ find contiguous range that adds up to a given value. """
    for size in range(2, len(numbers)):
        for sequence in iter_contiguous(numbers, size):
            if sum(sequence) == target_value:
                return sequence


def get_weakness(numbers):
    """ get the weakness of a contiguous range. """
    return min(numbers) + max(numbers)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')
default_preamble_size = 25


def main(inargs=None):
    filename, size = (sys.argv + [default_input_file,
                                  default_preamble_size])[1:3]
    size = int(size)

    with open(filename) as f:
        numbers = tuple(read_numbers(f))

    invalid = next(get_invalid_values(numbers, size))
    print(f"Part 1: {invalid}")

    score = get_weakness(find_range(numbers, invalid))
    print(f"Part 2: {score}")


if __name__ == '__main__':
    main()
