"""
Advent of Code 2023

`Day 15 <https://adventofcode.com/2023/day/15>`_:
Lens Library
"""
import os
import re
import sys


def read_input(fd):
    """ Read input from file-like *fd*. """
    for line in fd:
        for inst in line.strip().split(","):
            yield inst


def get_hash(value, current=0):
    """ Get hash for a given value. """
    for char in value:
        current = (current + ord(char.encode('ascii'))) * 17 % 256
    return current


def solve_pt1(values):
    return sum(get_hash(value) for value in values)


class Box(object):

    def __init__(self, box_number):
        self.box_number = box_number
        self.lens_order = []
        self.lens_focus = {}

    def __len__(self):
        """ Get number of lenses in box. """
        return len(self.lens_order)

    def __iter__(self):
        """ Iterate over lens labels in order. """
        return iter(self.lens_order)

    def __setitem__(self, item, value):
        """ Add or update focal length *value* for lens with label *item*. """
        if item not in self.lens_focus:
            self.lens_order.append(item)
        self.lens_focus[item] = value

    def __delitem__(self, item):
        """ Remove lens with label *item* from box. """
        if self.lens_focus.pop(item, None) is not None:
            self.lens_order.remove(item)

    def __int__(self):
        """ Total focal power of this box. """
        return sum((self.box_number + 1) * lens_number * self.lens_focus[label]
                   for lens_number, label in enumerate(self, 1))


RE_INST = re.compile(r"^([a-z]+)(=[1-9]|-)$")


def parse_instruction(instruction):
    """ Split instruction into (label, operation, focal length) tuple. """
    label, rest = RE_INST.match(instruction).groups()
    if rest == "-":
        return label, "-", 0
    else:
        return label, "=", int(rest[1:])


def solve_pt2(values):
    boxes = [Box(i) for i in range(256)]
    instructions = list(parse_instruction(v) for v in values)

    # Run instructions
    for label, op, arg in instructions:
        box = boxes[get_hash(label)]
        if op == "=":
            box[label] = arg
        else:
            del box[label]

    return sum(int(box) for box in boxes)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = list(read_input(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
