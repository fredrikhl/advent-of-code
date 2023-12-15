"""
Advent of Code 2023

`Day 7 <https://adventofcode.com/2023/day/7>`_:
Camel Cards
"""
import collections
import functools
import itertools
import os
import re
import sys

# Input cards in value order low to high
CARDS = "23456789TJQKA"

# J can be a wildcard - we then replace it with X when scoring highcards
WILDCARD = ("J", "X")

# Valid hand type signatures (most common, second most common)
HAND_TYPES = (
    (1, 1),  # high card
    (2, 1),  # one pair
    (2, 2),  # two pairs
    (3, 1),  # three of a kind
    (3, 2),  # full house
    (4, 1),  # four of a kind
    (5, 0),  # five of a kind
)

CARD_SCORES = {c: i for i, c in enumerate(WILDCARD[1] + CARDS, 1)}
HAND_SCORES = {c: s for s, c in enumerate(HAND_TYPES, 1)}

HAND_REGEX = re.compile(r"([%s]{5})\s+(\d+)" % (CARDS,))


def parse_line(value):
    hand, bid = HAND_REGEX.match(value).groups()
    return hand, int(bid)


def read_input(fd):
    """ Read input from file-like *fd*. """
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            yield parse_line(line)
        except Exception as e:
            raise ValueError("Invalid value on line %d: %s (%s)"
                             % (lineno, repr(line), e))


def get_hand_key(hand, wildcard=False):
    """
    Get a hand representation tuple for use in comparisons.

    # three of a kind
    >>> get_hand_key("QQQJA")
    (4, 12, 12, 12, 11, 14)

    # wildcards - four of a kind, but jacks are worth 1
    >>> get_hand_key("QQQJA", wildcard=True)
    (6, 12, 12, 12, 1, 14)
    """
    if wildcard:
        cards = hand.replace(*WILDCARD)
        hand = get_best_hand(hand)
    else:
        cards = hand
    hand_value = HAND_SCORES[get_hand_type(hand)]
    card_values = tuple(CARD_SCORES[c] for c in cards)
    return (hand_value,) + card_values


def get_hand_type(hand):
    """ Get the hand type of a given *hand*. """
    count = collections.Counter(hand)
    return (tuple(n for _, n in count.most_common(2)) + (0, 0))[:2]


def get_best_hand(hand):
    """ Get the best possible hand with jacks as wildcards. """
    hands = list(get_wildcard_alternatives(hand))
    # we use `get_hand_key` here, but in practice it only scores the hand type.
    # We *could* use `lambda hand: HAND_SCORES[get_hand_type(hand)]`
    for best in sorted(hands, key=get_hand_key, reverse=True):
        return best


def get_wildcard_alternatives(hand):
    """ Get all possible hands with wildcards replaced. """
    num_jacks = hand.count(WILDCARD[0])
    alternatives = set(c for c in CARDS if c != WILDCARD[0])
    # We'd normally need the product here:
    #   `itertools.product(alternatives, repeat=num_jacks)`
    # but card order isn't relevant when scoring hand types, and the
    # best hand type result isn't used for tie breaks.
    for combo in itertools.combinations_with_replacement(alternatives,
                                                         num_jacks):
        candidate = hand
        for card in combo:
            candidate = candidate.replace(WILDCARD[0], card, 1)
        yield candidate


def solve(values, wildcard=False):
    """ Get total winnings from hand rank and bids. """
    by_rank = sorted(values,
                     key=lambda p: get_hand_key(p[0], wildcard=wildcard))
    return sum(rank * bid for rank, (_, bid) in enumerate(by_rank, 1))


solve_pt1 = functools.partial(solve, wildcard=False)
solve_pt2 = functools.partial(solve, wildcard=True)
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
