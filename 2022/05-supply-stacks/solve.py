""" Advent of Code 2022

`Day 5 <https://adventofcode.com/2022/day/5>`_:
Supply Stacks
"""
import collections
import functools
import os
import re
import sys


RE_ROW = re.compile(r"(?:\[([A-Z])\]|   )[ ]?")
RE_IDX = re.compile(r"\s*(?:(\d+)\s*)")
RE_OP = re.compile(r"move (\d+) from (\d+) to (\d+)")


def read_input(fd):
    """ Read starting arrangement and instructions from file. """
    rows = []
    names = None
    ops = []

    lineno = 0
    line = ""
    try:
        # Read stack rows and indices
        for lineno, line in enumerate(fd, 1):
            if '[' in line:
                rows.append(tuple(RE_ROW.findall(line.rstrip("\n"))))
            else:
                names = tuple(int(i)
                              for i in RE_IDX.findall(line.rstrip("\n")))
                break

        # Skip empty line separator
        line = next(fd)
        lineno += 1
        if line != "\n":
            raise ValueError('expected empty line')

        # Read instructions
        for lineno, line in enumerate(fd, lineno):
            ops.append(
                tuple(int(i) for i in RE_OP.match(line.rstrip("\n")).groups()))
    except Exception as e:
        raise ValueError('invalid value on line %d (%r): %s' %
                         (lineno, line, e))
    return names, tuple(rows), tuple(ops)


class Stacks(object):
    """ Stacks of crates.  """

    def __init__(self, stack_names):
        self.names = stack_names
        self._stacks = {n: collections.deque() for n in stack_names}

    @property
    def top_row(self):
        """ Row of crates from the top of each stack. """
        return tuple(self._stacks[i][-1] if self._stacks[i] else " "
                     for i in self.names)

    def move(self, num, from_stack, to_stack, group=False):
        """ Move *num* crates from *from_stack* to *to_stack*. """
        if from_stack not in self._stacks:
            raise ValueError("invalid op: invalid from-stack: "
                             + repr(from_stack))
        if to_stack not in self._stacks:
            raise ValueError("invalid op: invalid to-stack: "
                             + repr(to_stack))
        if len(self._stacks[from_stack]) < num:
            raise ValueError("invalid op: from-stack too short: %r (%r)"
                             % (from_stack, num))

        buffer = []
        for _ in range(num):
            # remove crates in order from top of stack
            buffer.append(self._stacks[from_stack].pop())
        if group:
            # invert order
            buffer = reversed(buffer)
        # add crates to top of stack, last one in buffer on top
        self._stacks[to_stack].extend(buffer)

    @classmethod
    def from_rows(cls, names, rows):
        """ Create stacks from *rows* of crates. """
        obj = cls(names)
        for row in rows:
            if len(row) > len(names):
                raise ValueError("invalid row length")
            for name, value in zip(names, row):
                if value:
                    # add crate from row to bottom of stack
                    obj._stacks[name].appendleft(value)
        return obj


def solve(stacks, ops, group):
    """
    :type stacks: Stacks
    :param iterable ops:
        tuples of (number of crates, from_stack name, to_stack name)
    :param bool group:
        If all crates should be moved as a single group (part 2)
    """
    for num, from_stack, to_stack in ops:
        stacks.move(num, from_stack, to_stack, group=group)
    return "".join(stacks.top_row)


solve_pt1 = functools.partial(solve, group=False)
solve_pt2 = functools.partial(solve, group=True)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            names, rows, ops = read_input(f)

        pt1 = solve_pt1(Stacks.from_rows(names, rows), ops)
        print('Part 1:', pt1)

        pt2 = solve_pt2(Stacks.from_rows(names, rows), ops)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
