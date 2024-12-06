"""
Advent of Code 2024

`Day 6 <https://adventofcode.com/2024/day/6>`_:
Guard Gallivant
"""
import os
import sys

_UP = (-1, 0)
_DOWN = (1, 0)
_LEFT = (0, -1)
_RIGHT = (0, 1)

HEADINGS = {'^': _UP, '>': _RIGHT, 'v': _DOWN, '<': _LEFT}
BLOCK = '#'
SPACE = '.'

NEXT_HEADING = {_UP: _RIGHT, _RIGHT: _DOWN, _DOWN: _LEFT, _LEFT: _UP}


def read_map(f):
    """ read position and letter pairs from file-like *f*. """
    rownum = 0
    for lineno, line in enumerate(f, 1):
        if not line.strip():
            continue
        for colnum, char in enumerate(line.strip()):
            if char in HEADINGS or char in (BLOCK, SPACE):
                yield ((rownum, colnum), char)
            else:
                raise ValueError("invalid input on line %d (%r): %r"
                                 % (lineno, line, char))
        rownum += 1


def find_start(layout):
    """ find start position and heading in *layout*. """
    for pos, char in layout.items():
        if char in HEADINGS:
            return (pos, HEADINGS[char])
    # check for multiple start locations?
    raise ValueError("no start position in input")


def walk(start, layout):
    """ follow the patrol path of a guard """
    pos, head = start
    while pos in layout:
        yield (pos, head)
        for _ in NEXT_HEADING:
            nextpos = (pos[0] + head[0], pos[1] + head[1])
            if layout.get(nextpos) == BLOCK:
                head = NEXT_HEADING[head]
                continue
            pos = nextpos
            break
        else:
            # only possible if we start in a position surrounded by blocks
            raise RuntimeError("no valid steps at position=%s, heading=%s"
                               % (repr(pos), repr(head)))


def is_loop(start, layout):
    """ check if the path starting at *start* in *layout* is a loop """
    seen = set()
    for state in walk(start, layout):
        if state in seen:
            return True
        seen.add(state)
    return False


def solve_pt1(start, layout):
    """ count number of visited positions before leaving the *layout* """
    return len(set(pos for pos, _ in walk(start, layout)))


def solve_pt2(start, layout):
    """ count number of layouts with one extra block that creates a loop """
    layout = dict(layout)
    candidates = set(p for p, v in layout.items() if v == SPACE)
    loops = 0
    for pos in candidates:
        oldval, layout[pos] = layout[pos], BLOCK
        loops += is_loop(start, layout)
        layout[pos] = oldval
    return loops


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            layout = dict(read_map(f))

        start = find_start(layout)

        # input sanity check
        if is_loop(start, layout):
            raise RuntimeError("initial input path is a loop!")

        pt1 = solve_pt1(start, layout)
        print("Part 1:", pt1)

        pt2 = solve_pt2(start, layout)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
