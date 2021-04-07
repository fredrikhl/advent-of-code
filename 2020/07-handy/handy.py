"""
AoC Day 7: Handy Haversacks
"""
import re
import os
import sys


line_regex = re.compile(r"(\w+ \w+) bags contain ([^\.]+)\.")
item_regex = re.compile(r"(\d+) (\w+ \w+) bags?")


def parse_rule(line):
    """ parse a single rule line. """
    container, items = line_regex.fullmatch(line.rstrip('\n')).groups()
    content = {}
    if items != 'no other bags':
        for raw_item in items.split(', '):
            num, item = item_regex.fullmatch(raw_item).groups()
            if item in content:
                raise ValueError('duplicate rule for %r (%r)' %
                                 (container, item))
            content[item] = int(num)
    return container, content


def read_rules(fd):
    """ read and parse rules from a file-like object. """
    rules = {}
    for lineno, line in enumerate(fd, 1):
        try:
            container, content = parse_rule(line.rstrip('\n'))
            if container in content:
                raise ValueError('duplicate rule %r' % container)
            rules[container] = content
        except Exception as e:
            raise ValueError('error on line %d (%r): %s' % (lineno, line, e))
    return rules


def reverse_rules(rules):
    """ make a mapping from bag to possible container bags.

    >>> reverse_rules({'a': {'b': 1, 'c': 2}})
    {'b': {'a': 1}, 'c': {'a': 2}}
    """
    parents = {}
    for parent, children in rules.items():
        for child, count in children.items():
            parents.setdefault(child, {})[parent] = count
    return parents


def _find_containers(parent_map, bags):
    for parent in parent_map.get(bags[-1], ()):
        if parent in bags:
            # we've already dealt with this bag
            raise ValueError('cycle detected: ' + repr(bags + (parent,)))

        # 'parent' can hold our bags
        yield bags + (parent,)
        # whatever can hold parent can also hold our bags
        yield from _find_containers(parent_map, bags + (parent,))


def count_containers(rules, bag):
    """ find all bags that can contain *bag* somewhere. """
    parent_map = reverse_rules(rules)
    containers = set(bags[-1]
                     for bags in _find_containers(parent_map, (bag,)))
    return len(containers)


def _generate_counts(rules, bags, n):
    current = bags[-1]

    for child in rules.get(current, ()):
        if child in bags:
            # we've already counted this bag
            raise ValueError('cycle detected: ' + repr(bags + (child,)))

        total = rules[current][child] * n
        yield total

        # child may contain other bags as well
        yield from _generate_counts(rules, bags + (child,), total)


def count_bags(rules, bag):
    """ count total number of bags in *bag*. """
    return sum(_generate_counts(rules, (bag,), 1))


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        rules = read_rules(f)

    num = count_containers(rules, 'shiny gold')
    print(f'Part 1: {num}')

    count = count_bags(rules, 'shiny gold')
    print(f'Part 2: {count}')


if __name__ == '__main__':
    main()
