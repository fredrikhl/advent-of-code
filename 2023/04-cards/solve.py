"""
Advent of Code 2023

`Day 4 <https://adventofcode.com/2023/day/4>`_:
Scratchcards
"""
import os
import re
import sys


def read_cards(fd):
    """ Read lottery cards from file-like *fd*. """
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            yield parse_card(line)
        except Exception as e:
            raise ValueError("Invalid card on line %d: %s (%s)"
                             % (lineno, repr(line), e))


RE_CARD = re.compile(r"Card\s+(\d+): ([^|]+) \| (.*)")
RE_NUMS = re.compile(r"\d+")


def parse_card(value):
    """ Get card number, played numbers, and winning numbers from line. """
    raw_cardno, raw_nums, raw_winners = RE_CARD.match(value).groups()
    cardno = int(raw_cardno)
    numbers = set(int(n) for n in RE_NUMS.findall(raw_nums))
    winners = set(int(n) for n in RE_NUMS.findall(raw_winners))
    return cardno, numbers, winners


def get_points(n_matches):
    """ Get number of points for a given number of matches. """
    return 2 ** (n_matches - 1) if n_matches else 0


def solve_pt1(cards):
    """ Get total number of points on all cards. """
    return sum(get_points(len(numbers & winners))
               for _, numbers, winners in cards)


def solve_pt2(cards):
    """ Get total number of cards seen. """
    # map of how many new cards any given card will win
    win_graph = {cardno: len(numbers & winners)
                 for cardno, numbers, winners in cards}

    # we start out with one of each of the input cards
    inventory = {cardno: 1 for cardno in win_graph}

    # and keep a running total of seen cards
    total_cards = len(inventory)

    while inventory:
        # calculate new inventory from number of cards won in current
        # inventory, and update running total
        new_inventory = {}
        for cardno, count in inventory.items():
            wins = win_graph.get(cardno, 0)
            for new_card in range(cardno + 1, cardno + 1 + wins):
                if new_card in new_inventory:
                    new_inventory[new_card] += count
                else:
                    new_inventory[new_card] = count
                total_cards += count
        inventory = new_inventory

    return total_cards


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            cards = list(read_cards(f))

        pt1 = solve_pt1(cards)
        print('Part 1:', pt1)

        pt2 = solve_pt2(cards)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
