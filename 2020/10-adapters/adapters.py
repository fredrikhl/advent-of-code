import collections
import os
import sys


def read_numbers(fd):
    """ read numbers from a file-like object. """
    for lineno, line in enumerate(fd, 1):
        try:
            yield int(line.rstrip())
        except Exception as e:
            raise ValueError('error on line %d (%r): %s' % (lineno, line, e))


def find_all_jumps(numbers, max_delta=3, init=0):
    """ Find differences when connecting all adapters. """
    prev = init
    for curr in (sorted(numbers) + [max(numbers) + max_delta]):
        diff = curr - prev
        if diff > max_delta:
            raise ValueError('no connection from %d to %d (max: %d))' %
                             (prev, curr, max_delta))
        yield diff
        prev = curr


def solve_score(numbers):
    """ Get the score for part 1. """
    jump_count = collections.Counter(find_all_jumps(numbers))
    return jump_count[1] * jump_count[3]


def gen_jump_table(numbers, max_delta=3, init=0):
    """ Get a jump table for all possible jumps. """
    nodes = [init] + sorted(numbers) + [max(numbers) + max_delta]

    for idx, value in enumerate(nodes[:-1]):
        yield value, tuple(v for v in nodes[idx+1:] if v <= value + max_delta)


def count_combinations(numbers):
    """ solve part 1 """
    jumps = dict(gen_jump_table(numbers))
    counts = {}
    for v in reversed(sorted(jumps)):
        counts[v] = sum(counts.get(opt, 1) for opt in jumps[v])
    return counts[min(jumps)]


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main(inargs=None):
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        numbers = tuple(read_numbers(f))

    score = solve_score(numbers)
    print(f"Part 1: {score}")

    count = count_combinations(numbers)
    print(f"Part 2: {count}")


if __name__ == '__main__':
    main()
