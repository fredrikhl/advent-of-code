"""
Advent of Code 2024

`Day 9 <https://adventofcode.com/2024/day/9>`_:
Disk Fragmenter
"""
import os
import sys


def read_input(f):
    """ read position and letter pairs from file-like *f*. """
    return [int(i) for i in f.readline().strip()]


def checksum(iterable):
    """ get checksum from an *iterable* of file blocks (block-id, file-id) """
    return sum(block_id * file_id for block_id, file_id in iterable if file_id)


def iter_blocks(disk_map, reverse=False):
    """" get the content of each block on the disk. """
    iterable = reversed(disk_map) if reverse else disk_map
    node_id = len(disk_map) - 1 if reverse else 0
    for size in iterable:
        file_id = None if node_id % 2 else node_id // 2
        for _ in range(size):
            yield file_id
        node_id += -1 if reverse else 1


def defrag_blocks(disk_map):
    """ move file blocks from the end into the first available space. """
    blocks = iter_blocks(disk_map)
    to_move = iter_blocks(disk_map, reverse=True)
    file_blocks = sum(size for node_id, size in enumerate(disk_map)
                      if not node_id % 2)
    for block_id in range(0, file_blocks):
        file_id = next(blocks)
        while file_id is None:
            file_id = next(to_move)
        yield block_id, file_id


def solve_pt1(disk_map):
    return checksum(defrag_blocks(disk_map))


def defrag_files(disk_map):
    """ move whole files from the end into the first available space. """
    spaces = []
    files = []

    block_id = 0
    for node_id, size in enumerate(disk_map):
        if node_id % 2:
            spaces.append((block_id, size))
        else:
            files.append((block_id, size, node_id // 2))
        block_id += size

    def reserve_blocks(block_id, size):
        """ reserve blocks for a file at *block_id* of *size*. """
        for idx, (next_id, next_size) in enumerate(spaces):
            if next_id > block_id:
                break
            if next_size < size:
                continue
            if next_size > size:
                spaces[idx] = (next_id + size, next_size - size)
            else:
                spaces.pop(idx)
            return next_id
        return block_id

    for block_id, size, file_id in reversed(files):
        block_id = reserve_blocks(block_id, size)
        for i in range(size):
            yield block_id + i, file_id


def solve_pt2(disk_map):
    return checksum(defrag_files(disk_map))


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            data = read_input(f)

        pt1 = solve_pt1(data)
        print("Part 1:", pt1)

        pt2 = solve_pt2(data)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
