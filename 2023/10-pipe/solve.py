"""
Advent of Code 2023

`Day 10 <https://adventofcode.com/2023/day/10>`_:
Pipe Maze
"""
import os
import sys


# Direction deltas
DIRECTIONS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

# Pipe to direction deltas
PIPES = {
    "|": set((DIRECTIONS['N'], DIRECTIONS['S'])),
    "-": set((DIRECTIONS['E'], DIRECTIONS['W'])),
    "L": set((DIRECTIONS['N'], DIRECTIONS['E'])),
    "J": set((DIRECTIONS['N'], DIRECTIONS['W'])),
    "7": set((DIRECTIONS['S'], DIRECTIONS['W'])),
    "F": set((DIRECTIONS['S'], DIRECTIONS['E'])),
}


def read_matrix(fd):
    """ Read position and value from file-like *fd*. """
    rownum = 0
    for lineno, line in enumerate(fd, 1):
        if not line.strip():
            continue
        try:
            row = tuple(line.strip())
            for colnum, char in enumerate(row):
                yield (rownum, colnum), char
            rownum += 1
        except Exception as e:
            raise ValueError('invalid input on line %d (%r): %s' %
                             (lineno, line, e))


def add_delta(pos, delta):
    """ Get a new position from a position and delta. """
    return tuple(a + b for a, b in zip(pos, delta))


def calculate_pipe(matrix, pos):
    """ Get the correct pipe character from neighbors in a given *pos*. """
    # 1. Find deltas to the neighbors that actually connect back to *pos*
    candidate = set()
    for delta in DIRECTIONS.values():
        npos = add_delta(pos, delta)
        if matrix.get(npos) not in PIPES:
            continue
        for ndelta in PIPES[matrix[npos]]:
            if pos == add_delta(npos, ndelta):
                candidate.add(delta)

    # 3. Find the correct pipe character with those deltas (connections)
    for char, deltas in PIPES.items():
        if candidate == deltas:
            return char
    raise ValueError("no possible pipe in position: " + repr(pos))


def replace_start(matrix):
    """ Get start point, and replace missing start char. """
    # Find the start position
    for start, value in matrix.items():
        if value == "S":
            break
    else:
        raise ValueError("no starting position")

    matrix = dict(matrix)
    matrix[start] = calculate_pipe(matrix, start)
    return start, matrix


def get_next(matrix, prev, curr):
    """ Get next position following a path. """
    cands = set(add_delta(curr, d) for d in set(PIPES[matrix[curr]]))
    # should result in two positions:
    # discard the one we came from, and return the other.
    cands.discard(prev)
    return cands.pop()


def follow_path(matrix, curr):
    """ Walk the path from a given point. """
    seen = set()
    # We need to pick an initial direction, but we don't really care which.
    prev = add_delta(curr, next(iter(PIPES[matrix[curr]])))
    while curr not in seen:
        seen.add(curr)
        yield curr
        prev, curr = curr, get_next(matrix, prev, curr)


def solve_pt1(matrix):
    start, matrix = replace_start(matrix)
    # our path *should* be a loop, so the halfway point is the furthest away
    return len(list(follow_path(matrix, start))) // 2


def path_contains(path, pos, include_path=False):
    """
    Figure out if a given *pos* is contained by *path*.

    This is an implementation of the *even-odd rule* algorithm.
    """
    is_contained = False
    prev = path[-1]
    for curr in path:
        if (pos == curr):
            # this point is obviously on our path
            return include_path
        if (curr[1] > pos[1]) != (prev[1] > pos[1]):
            # We've crossed the path
            slope = ((pos[0] - curr[0]) * (prev[1] - curr[1])
                     - (pos[1] - curr[1]) * (prev[0] - curr[0]))
            if slope == 0:
                # this point is on our path
                return include_path
            if (slope < 0) != (prev[1] < curr[1]):
                is_contained = not is_contained
        prev = curr
    return is_contained


def solve_pt2(matrix):
    start, matrix = replace_start(matrix)
    path = list(follow_path(matrix, start))

    # speed-up: we-re not interested in points *on* our path,
    # so we don't need to check those:
    candidates = set(matrix) - set(path)

    return sum(path_contains(path, pos)
               for pos in candidates)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = dict(read_matrix(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
