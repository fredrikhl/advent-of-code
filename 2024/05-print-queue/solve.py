"""
Advent of Code 2024

`Day 5 <https://adventofcode.com/2024/day/5>`_:
Print Queue
"""
import os
import sys


def read_input(f):
    """ read rules and update sequences from file-like *f* """
    rules = []
    updates = []
    for lineno, line in enumerate(f, 1):
        if not line.strip():
            continue
        try:
            if "," in line:
                updates.append([int(i) for i in line.split(",")])
                continue

            if updates:
                raise ValueError("non-update content after update")

            if "|" in line:
                a, b = (int(i) for i in line.split("|"))
                rules.append((a, b))
                continue
        except Exception as e:
            raise ValueError('invalid input on line %d (%r): %s' %
                             (lineno, line, e))
    return rules, updates


class _Key(object):

    def __init__(self, after, value):
        self.after = after
        self.value = value

    def __lt__(self, other):
        return (self.value in self.after
                and other.value in self.after[self.value])


class RuleSet(object):
    """ a set of rules to sort a sequence """

    def __init__(self, rules):
        self._after = {}
        for a, b in rules:
            if a in self._after:
                self._after[a].add(b)
            else:
                self._after[a] = set((b,))

    def _keyfunc(self, value):
        return _Key(self._after, value)

    def sort(self, sequence):
        return sorted(sequence, key=self._keyfunc)


def get_middle(sequence):
    """ get the middle value of a *sequence* """
    return sequence[(len(sequence) // 2)]


def solve_pt1(ruleset, updates):
    fixed_updates = (ruleset.sort(update) for update in updates)
    return sum(
        get_middle(orig)
        for orig, fixed in zip(updates, fixed_updates)
        if orig == fixed
    )


def solve_pt2(ruleset, updates):
    fixed_updates = (ruleset.sort(update) for update in updates)
    return sum(
        get_middle(fixed)
        for orig, fixed in zip(updates, fixed_updates)
        if orig != fixed
    )


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            rules, updates = read_input(f)

        ruleset = RuleSet(rules)

        pt1 = solve_pt1(ruleset, updates)
        print("Part 1:", pt1)

        pt2 = solve_pt2(ruleset, updates)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
