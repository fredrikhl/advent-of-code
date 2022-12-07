""" Advent of Code 2022

`Day 7 <https://adventofcode.com/2022/day/7>`_:
No Space Left On Device
"""
import collections
import os
import sys


def read_input(fd):
    """ Read and parse file paths and sizes in terminal output from file. """
    expect_output = False
    path = tuple()
    for lineno, raw_line in enumerate(fd, 1):
        if not (line := raw_line.rstrip("\n")):
            continue
        try:
            if line.startswith("$ cd "):
                name = line[5:]
                if name == "/":
                    path = ("/",)
                elif name == "..":
                    path = path[:-1]
                else:
                    path = path + (name,)
                expect_output = False
                continue

            if line == "$ ls":
                expect_output = True
                continue

            if not expect_output:
                raise ValueError("unexpected output")

            if line.startswith("dir "):
                continue

            size, name = line.split(" ", 1)
            yield path + (name,), int(size)

        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def collect_sizes(values):
    """ Collect total size for each directory.  """
    dirs = collections.Counter()
    for path_t, size in values:
        # for each parent, add size to path index:
        while (path_t := path_t[:-1]):
            dirs[os.path.join(*path_t)] += size
    return dirs


THRESHOLD = 100000


def solve_pt1(paths):
    return sum(size for size in paths.values() if size <= THRESHOLD)


TOTAL_SIZE = 70000000
REQUIRE_FREE = 30000000


def solve_pt2(paths):
    curr_used = paths["/"]
    curr_free = TOTAL_SIZE - curr_used
    must_free = REQUIRE_FREE - curr_free
    return min(size for size in paths.values() if size >= must_free)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = collect_sizes(read_input(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
