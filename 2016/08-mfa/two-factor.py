"""
AoC Day 8: Two-Factor Authentication
"""
import argparse
import collections
import re
import os
import sys

COLS = 50
ROWS = 6


class Display(object):

    charmap = {True: '#', False: '.'}

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self._pixels = {i: False for i in range(cols * rows)}

    def rect(self, w, h):
        """ draw a w * h rectangle in upper left column. """
        for colnum in range(w):
            for rownum in range(h):
                self._pixels[rownum * self.cols + colnum] = True

    def shift_row(self, rownum, n):
        indexes = tuple(rownum * self.cols + offset
                        for offset in range(self.cols))
        tmprow = collections.deque(self._pixels[i] for i in indexes)
        tmprow.rotate(n)
        self._pixels.update(zip(indexes, tmprow))

    def shift_col(self, colnum, n):
        indexes = tuple(rownum * self.cols + colnum for rownum in range(self.rows))
        tmpcol = collections.deque(self._pixels[i] for i in indexes)
        tmpcol.rotate(n)
        self._pixels.update(zip(indexes, tmpcol))

    def count_lit(self):
        return sum(self._pixels.values())

    def to_string(self):
        return "\n".join(
            "".join(self.charmap[self._pixels[rownum * self.cols + colnum]]
                    for colnum in range(self.cols))
            for rownum in range(self.rows))




class _Op(object):

    _opmap = (
        (re.compile(r"^rect (\d+)x(\d+)$"), Display.rect),
        (re.compile(r"^rotate row y=(\d+) by (\d+)$"), Display.shift_row),
        (re.compile(r"^rotate column x=(\d+) by (\d+)$"), Display.shift_col),
    )

    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

    def __call__(self, display):
        self.fn(display, *self.args)

    @classmethod
    def parse(cls, value):
        for regex, op in cls._opmap:
            match = regex.match(value)
            if match:
                args = tuple(int(arg) for arg in match.groups())
                return cls(op, args)
        raise ValueError("invalid op: " + repr(value))


def read_ops(fd):
    for lineno, line in enumerate(fd, 1):
        try:
            yield _Op.parse(line.rstrip())
        except Exception as e:
            raise ValueError("invalid op on line %d: %s"
                             % (lineno, e))


def run_ops(display, ops):
    for opnum, op in enumerate(ops, 1):
        try:
            op(display)
        except Exception as e:
            raise RuntimeError("error in op %d: %s"
                               % (opnum, e))


def demo():
    s = Display(7, 3)

    print("rect 3x2")
    s.rect(3, 2)
    print(s.to_string())

    print("\nrotate column x=1 by 1")
    s.shift_col(1, 1)
    print(s.to_string())

    print("\nrotate row y=0 by 4")
    s.shift_row(0, 4)
    print(s.to_string())

    print("\nrotate column x=1 by 1")
    s.shift_col(1, 1)
    print(s.to_string())


def solve(filename):
    with open(filename) as f:
        ops = tuple(read_ops(f))

    display = Display(COLS, ROWS)
    run_ops(display, ops)

    num_lit = display.count_lit()
    print(f'Part 1: {num_lit} pixels')
    print("Part 2:", display.to_string(), sep="\n")


default_input_file = 'input.txt'
parser = argparse.ArgumentParser()
arg_mutex = parser.add_mutually_exclusive_group(required=True)
arg_mutex.add_argument('--solve', metavar='FILE', dest='solve_file')
arg_mutex.add_argument('--demo', action='store_true', dest='show_demo')


def main():
    args = parser.parse_args()

    if args.solve_file:
        solve(args.solve_file)

    if args.show_demo:
        demo()


if __name__ == '__main__':
    main()
