""" Advent of Code 2022

`Day 10 <https://adventofcode.com/2022/day/10>`_:
Cathode-Ray Tube
"""
import os
import sys


class Noop(object):
    """ Noop instruction. """
    cost = 1

    def __call__(self, value):
        return value


class Add(Noop):
    """ Add instruction. """
    cost = 2

    def __init__(self, term):
        self.term = term

    def __call__(self, value):
        return value + self.term


def read_input(fd):
    """ Read and parse input from file. """
    for lineno, raw_line in enumerate(fd, 1):
        if not (line := raw_line.strip()):
            continue
        try:
            if line.startswith('addx '):
                yield Add(int(line[5:]))
            elif line == 'noop':
                yield Noop()
            else:
                raise ValueError("unknown operation: " + repr(line))
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def iter_program(instructions):
    """ Step through a program and get the value for each tick. """
    ticks = 0
    value = 1
    for inst in instructions:
        for _ in range(inst.cost):
            ticks += 1
            yield ticks, value
        value = inst(value)


def solve_pt1(instructions):
    breaks = (20, 60, 100, 140, 180, 220)

    return sum(ticks * value
               for ticks, value in iter_program(instructions)
               if ticks in breaks)


def get_scanlines(instructions):
    buffer = []
    for ticks, value in iter_program(instructions):
        position = (ticks - 1) % 40
        sprite = (value - 1, value, value + 1)
        buffer.append("#" if position in sprite else ".")
        if ticks % 40 == 0:
            yield "".join(buffer)
            buffer.clear()


def solve_pt2(instructions):
    return "\n".join(get_scanlines(instructions))


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            values = tuple(read_input(f))

        pt1 = solve_pt1(values)
        print("Part 1:", pt1)

        pt2 = solve_pt2(values)
        print("Part 2:", pt2, sep="\n")


if __name__ == '__main__':
    main()
