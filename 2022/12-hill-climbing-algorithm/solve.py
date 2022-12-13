""" Advent of Code 2022

`Day 12 <https://adventofcode.com/2022/day/12>`_:
Hill Climbing Algorithm
"""
import collections
import queue
import os
import sys
import string


HEIGHT_MAP = {c: i for i, c in enumerate(string.ascii_lowercase)}
HEIGHT_MAP.update({
    'S': 0,
    'E': len(HEIGHT_MAP) - 1,
})

MOVEMENTS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def read_input(fd):
    """ Read and parse input from file. """
    row = 0
    for lineno, raw_line in enumerate(fd, 1):
        if not (line := raw_line.strip()):
            continue
        try:
            for col, char in enumerate(line):
                if char not in HEIGHT_MAP:
                    raise ValueError("invalid char at pos %d: %r"
                                     % (col + 1, char))
                yield (row, col, char)
            row += 1
        except Exception as e:
            raise ValueError("invalid value on line %d (%r): %s" %
                             (lineno, line, e))


def get_matrix(input_data):
    """ Build a map of point -> height, and find start/end points. """
    start = None
    end = None
    matrix = {}
    for row, col, char in input_data:
        matrix[row, col] = HEIGHT_MAP[char]
        if char == 'S':
            start = (row, col)
        if char == 'E':
            end = (row, col)
    if not start or not end:
        raise ValueError("missing start/end")
    return matrix, start, end


def get_moves(matrix, current):
    """ Find all valid next points from *current*. """
    max_height = matrix[current] + 1
    for dx, dy in MOVEMENTS:
        p = current[0] + dx, current[1] + dy
        if p in matrix and matrix[p] <= max_height:
            yield p


def find_shortest_path(matrix, current, target):
    """ shortest path and cost using dijkstra and priority queue. """
    paths = {current: None}
    costs = {current: 0}
    seen = set((current,))
    priority = queue.PriorityQueue()
    priority.put((0, current))

    while current != target:
        cost, current = priority.get(block=False)

        for next_node in get_moves(matrix, current):
            if next_node in seen:
                continue
            next_cost = cost + 1
            paths[next_node] = current
            costs[next_node] = next_cost
            priority.put((next_cost, next_node))
            seen.add(next_node)

    path = collections.deque()
    while current is not None:
        path.appendleft(current)
        current = paths[current]
    return tuple(path), costs[path[-1]]


def solve(matrix, start, end):
    """ Find length of shortest path from *start* to *end* in *matrix*. """
    try:
        path, cost = find_shortest_path(matrix, start, end)
        return cost
    except queue.Empty:
        # no valid path from start to end
        return -1


def solve_pt1(values):
    matrix, start, end = values
    return solve(matrix, start, end)


def solve_pt2(values):
    matrix, _, end = values
    lowest = [p for p, h in matrix.items() if h == HEIGHT_MAP['a']]
    lengths = (solve(matrix, s, end) for s in lowest)
    return min(length for length in lengths if length > 0)


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            values = get_matrix(read_input(f))

        pt1 = solve_pt1(values)
        print("Part 1:", pt1)

        pt2 = solve_pt2(values)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
