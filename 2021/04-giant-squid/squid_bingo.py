""" Advent of Code 2021

`Day 4 <http://adventofcode.com/2021/day/4>`_:
Giant Squid
"""
import os
import sys


def _parse_draws(line):
    try:
        return tuple(int(d) for d in line.strip().split(','))
    except Exception as e:
        raise ValueError('invalid draws (%r): %s' % (line, e))


def _parse_boards(fd, lineno=0):
    nums = tuple()
    for lineno, line in enumerate(fd, lineno + 1):
        line = line.strip()
        if not line:
            continue
        try:
            nums += tuple(int(d) for d in line.split(' ')
                          if d.strip())
            if len(nums) > 25:
                raise ValueError('invalid board (size %d)' % len(nums))
            elif len(nums) == 25:
                yield nums
                nums = tuple()
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))
    if nums:
        raise ValueError('incomplete board on line %d' % (lineno))


def read_bingo(fd):
    draws = _parse_draws(fd.readline().strip())
    boards = _parse_boards(fd, lineno=1)
    return tuple(draws), tuple(boards)


class BoardState(object):

    rows = cols = 5

    def __init__(self, numbers):
        self.remaining = {}
        self.rowhits = [0] * self.rows
        self.colhits = [0] * self.cols
        for idx, val in enumerate(numbers):
            self.remaining[val] = (idx % self.cols, idx // self.cols)

    def _mark(self, number):
        if number in self.remaining:
            col, row = self.remaining.pop(number)
            self.rowhits[row] += 1
            self.colhits[col] += 1
            return True
        return False

    def _is_bingo(self):
        return (any(hits >= self.rows for hits in self.rowhits)
                or any(hits >= self.cols for hits in self.colhits))

    def check(self, number):
        return self._mark(number) and self._is_bingo()

    def get_score(self, draw):
        return sum(self.remaining.keys()) * draw


def draw_winners(boards, draws):
    players = [BoardState(board) for board in boards]
    for draw in draws:
        for player in tuple(players):
            if player.check(draw):
                yield player, draw
                players.remove(player)


def solve_pt1(boards, draws):
    for player, draw in draw_winners(boards, draws):
        return player.get_score(draw)

    raise RuntimeError('no winners')


def solve_pt2(boards, draws):
    last_winner = last_draw = None
    for last_winner, last_draw in draw_winners(boards, draws):
        continue

    if last_winner is None:
        raise RuntimeError('no winners')

    return last_winner.get_score(last_draw)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            draws, boards = read_bingo(f)

        pt1 = solve_pt1(boards, draws)
        print('Part 1:', pt1)
        pt2 = solve_pt2(boards, draws)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
