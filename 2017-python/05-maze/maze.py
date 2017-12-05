""" Advent of Code 2017

`Day 5 <http://adventofcode.com/2017/day/5>`_:
A Maze of Twisty Trampolines, All Alike
"""
from __future__ import print_function
import argparse
import io
import sys


try:
    # PY2 compat
    input = raw_input
except NameError:
    pass


# Example input, default if no argument is given
EXAMPLE = u"\n".join(str(i) for i in (0, 3, 0, 1, -3)) + "\n"


def run(instructions, strangeness=None):
    """ The jump algorithm.

    :param list instructions:
        A list of jump offsets. Note that the list will be modified in place.

    :param callable strangeness:
        If defined, a callable that generates new jump instructions.

    :return generator:
        Returns a generator with the program addresses and instructions.

        In each step of the program, this generator will yield a tuple with the
        current address and instruction from that address.
    """
    # initial address
    addr = 0

    while True:
        try:
            # jump to new address
            jump = instructions[addr]
        except IndexError:
            break

        if callable(strangeness):
            instructions[addr] = strangeness(jump)
        yield addr, jump
        addr = addr + jump


def part_1_modifier(jump):
    """ Increment jump instruction.

    Increments 'jump' by 1.

    :param int jump: the current jump value
    :return int: the new jump value
    """
    return jump + 1


def part_2_modifier(jump):
    """ Increment and decrement jump instruction.

    - decrements 'jump' by 1 if >= 3
    - increments 'jump' by 1 if < 3

    :param int jump: the current jump value
    :return int: the new jump value
    """
    return jump + (-1 if jump >= 3 else 1)


def count_steps(iterator):
    """ Run program to completion, and return number of steps. """
    for step, (addr, jump) in enumerate(iterator, 1):
        pass
    return step


def step_through(iterator):
    """ Run program in debug mode, with breakpoints. """
    def read_steps(default):
        return int(input('step [{0}]>'.format(default)) or default)

    steps = read_steps(1)
    break_at_step = steps
    for current_step, (addr, jump) in enumerate(iterator, 1):
        print("{0:08d}: {1:4d}  {2:+d}".format(current_step, addr, jump))
        if current_step == break_at_step:
            steps = read_steps(steps)
            break_at_step = current_step + steps
    return current_step


def main(inargs=None):
    parser = argparse.ArgumentParser()
    debug_arg = parser.add_argument(
        '-d', '--debug',
        action='store_const',
        dest='counter',
        const=step_through,
        default=count_steps,
        help="step through the program")
    skip = parser.add_mutually_exclusive_group()
    skip.add_argument(
        '--skip-part-1',
        dest='part_1',
        action='store_false',
        default=True,
        help="skip part 1")
    skip.add_argument(
        '--skip-part-2',
        dest='part_2',
        action='store_false',
        default=True,
        help="skip part 2")
    parser.add_argument(
        'program',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('Ur'),
        default=io.StringIO(EXAMPLE),
        help="program file, or '-' to read from STDIN")
    args = parser.parse_args(inargs)

    if args.program is sys.stdin and args.counter is debug_arg.const:
        raise argparse.ArgumentError(
            debug_arg,
            "cannot use debug mode when reading program from stdin")

    print("Reading program...")
    with args.program:
        instructions = [int(instruction)
                        for instruction in args.program.read().splitlines()
                        if instruction.strip()]

    print("Done, instructions: {0}".format(len(instructions)))

    if args.part_1:
        print("\nRunning Part 1...")
        steps = args.counter(run(instructions[:], part_1_modifier))
        print("Done, steps: {0}".format(steps))

    if args.part_2:
        print("\nRunning Part 2...")
        steps = args.counter(run(instructions[:], part_2_modifier))
        print("Done, steps: {0}".format(steps))


if __name__ == '__main__':
    main()
