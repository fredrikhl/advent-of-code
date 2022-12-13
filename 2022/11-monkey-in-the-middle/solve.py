""" Advent of Code 2022

`Day 11 <https://adventofcode.com/2022/day/11>`_:
Monkey In The Middle
"""
import collections
import functools
import operator
import os
import re
import sys


OPERATORS = {'+': operator.add, '*': operator.mul}


def get_operation(a, op, b):
    """ Get new worry level on inspection. """
    func = OPERATORS[op]
    a = None if a == "old" else int(a)
    b = None if b == "old" else int(b)

    def get_worry(value):
        return func(value if a is None else a, value if b is None else b)

    return get_worry


class Test(object):
    """ Get target monkey for a given worry level. """

    def __init__(self, divisor, on_true, on_false):
        self.divisor = int(divisor)
        self.on_true = int(on_true)
        self.on_false = int(on_false)

    def __call__(self, value):
        if value % self.divisor == 0:
            return self.on_true
        return self.on_false


class Monkey(object):
    """ A monkey representation. """

    def __init__(self, items, get_worry, get_target):
        self.items = collections.deque(items)
        self.get_worry = get_worry
        self.get_target = get_target

    def add(self, item):
        self.items.append(item)

    def inspect(self):
        while self.items:
            yield self.items.popleft()


re_monkey = re.compile(r"Monkey (\d+)")
re_items = re.compile(r"  Starting items: ([0-9, ]+)")
re_op = re.compile(r"  Operation: new = (old|\d+) ([+*]) (old|\d+)")
re_test = re.compile(r"  Test: divisible by (\d+)")
re_t = re.compile(r"    If true: throw to monkey (\d+)")
re_f = re.compile(r"    If false: throw to monkey (\d+)")


def read_input(fd):
    """ Read and parse input from file. """
    lines = enumerate(fd, 1)
    lineno = 0
    line = ""

    while True:
        try:
            lineno, line = next(lines)
        except StopIteration:
            break

        if not line.rstrip():
            continue

        try:
            monkey_id = int(re_monkey.match(line).group(1))

            lineno, line = next(lines)
            items = tuple(int(i)
                          for i in re_items.match(line).group(1).split(','))

            lineno, line = next(lines)
            get_worry = get_operation(*(re_op.match(line).groups()))

            lineno, line = next(lines)
            divisor = int(re_test.match(line).group(1))

            lineno, line = next(lines)
            on_true = int(re_t.match(line).group(1))
            if monkey_id == on_true:
                raise ValueError("Recursive monkey throw: " + repr(monkey_id))

            lineno, line = next(lines)
            on_false = int(re_f.match(line).group(1))
            if monkey_id == on_false:
                raise ValueError("Recursive monkey throw: " + repr(monkey_id))

            get_target = Test(divisor, on_true, on_false)
            yield monkey_id, items, get_worry, get_target
        except Exception as e:
            raise ValueError("invalid value on line %d (%r): %s" %
                             (lineno, line, e))


def solve(monkey_data, rounds, reduce_worry):
    monkeys = {m_id: Monkey(items, get_worry, get_target)
               for m_id, items, get_worry, get_target in monkey_data}
    order = sorted(monkeys)

    inspections = collections.Counter()

    for _ in range(rounds):
        for monkey_id in order:
            monkey = monkeys[monkey_id]
            for worry in monkey.inspect():
                new_worry = reduce_worry(monkey.get_worry(worry))
                new_id = monkey.get_target(new_worry)
                monkeys[new_id].add(new_worry)
                inspections[monkey_id] += 1

    most_active = tuple(num for m_id, num in inspections.most_common(2))
    return operator.mul(*most_active)


def solve_pt1(monkey_data):
    return solve(monkey_data, 20, lambda v: int(v // 3))


def solve_pt2(monkey_data):
    divisors = (t[3].divisor for t in monkey_data)
    common_divisor = functools.reduce(operator.mul, divisors, 1)
    return solve(monkey_data, 10000, lambda v: v % common_divisor)


default_input_file = os.path.join(os.path.dirname(__file__), "input.txt")


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * "\n" + "Solutions for", filename)
        with open(filename) as f:
            values = tuple(read_input(f))

        pt1 = solve_pt1(values)
        print("Part 1:", pt1)

        pt2 = solve_pt2(values)
        print("Part 2:", pt2)


if __name__ == "__main__":
    main()
