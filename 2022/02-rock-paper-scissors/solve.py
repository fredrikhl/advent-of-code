""" Advent of Code 2022

`Day 2 <https://adventofcode.com/2022/day/2>`_:
Rock Paper Scissors
"""
import enum
import os
import sys


class Hands(enum.IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(enum.IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6


OPPONENT_MAP = {"A": Hands.ROCK, "B": Hands.PAPER, "C": Hands.SCISSORS}
PLAYER_MAP = {"X": Hands.ROCK, "Y": Hands.PAPER, "Z": Hands.SCISSORS}
OUTCOME_MAP = {"X": Outcome.LOSS, "Y": Outcome.DRAW, "Z": Outcome.WIN}


def get_winning_hand(hand):
    """ Get the hand that beats *hand*. """
    return Hands(hand % 3 + 1)


def get_losing_hand(hand):
    """ Get hand that *hand* beats. """
    return Hands((hand - 2) % 3 + 1)


def get_outcome(player, opponent):
    """ Get outcome from given *player* *opponent* hands. """
    if player == opponent:
        return Outcome.DRAW
    elif player == get_winning_hand(opponent):
        return Outcome.WIN
    elif player == get_losing_hand(opponent):
        return Outcome.LOSS
    else:
        raise ValueError("Invalid player hand: " + repr(player))


def get_choice(outcome, opponent):
    """ Get player hand choice from wanted *outcome* and *opponent* hand. """
    if outcome == Outcome.DRAW:
        return opponent
    elif outcome == Outcome.WIN:
        return get_winning_hand(opponent)
    elif outcome == Outcome.LOSS:
        return get_losing_hand(opponent)
    else:
        raise ValueError("Invalid outcome: " + repr(outcome))


def read_pairs(fd):
    """ Read strategies from file. """
    for lineno, line in enumerate(fd, 1):
        try:
            opponent, sep, play = line.strip().partition(" ")
            if opponent not in OPPONENT_MAP:
                raise ValueError("invalid opponent value: " + repr(opponent))
            if play not in PLAYER_MAP:
                raise ValueError("invalid play value: " + repr(play))
            yield opponent, play
        except Exception as e:
            raise ValueError('invalid value on line %d (%r): %s' %
                             (lineno, line, e))


def solve_pt1(plays):
    return sum(
        get_outcome(PLAYER_MAP[player], OPPONENT_MAP[opponent])
        + PLAYER_MAP[player]
        for opponent, player in plays)


def solve_pt2(plays):
    return sum(
        get_choice(OUTCOME_MAP[outcome], OPPONENT_MAP[opponent])
        + OUTCOME_MAP[outcome]
        for opponent, outcome in plays)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            values = tuple(read_pairs(f))

        pt1 = solve_pt1(values)
        print('Part 1:', pt1)

        pt2 = solve_pt2(values)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
