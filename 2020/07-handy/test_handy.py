import io

import handy as mod

example_text = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip()

example_rules = {
    'light red': {'bright white': 1, 'muted yellow': 2},
    'dark orange': {'bright white': 3, 'muted yellow': 4},
    'bright white': {'shiny gold': 1},
    'muted yellow': {'shiny gold': 2, 'faded blue': 9},
    'shiny gold': {'dark olive': 1, 'vibrant plum': 2},
    'dark olive': {'faded blue': 3, 'dotted black': 4},
    'vibrant plum': {'faded blue': 5, 'dotted black': 6},
    'faded blue': {},
    'dotted black': {},
}


# inverted rules
example_parents = {
    'bright white': {'light red': 1, 'dark orange': 3},
    'muted yellow': {'light red': 2, 'dark orange': 4},
    'shiny gold': {'bright white': 1, 'muted yellow': 2},
    'faded blue': {'muted yellow': 9, 'dark olive': 3, 'vibrant plum': 5},
    'dark olive': {'shiny gold': 1},
    'vibrant plum': {'shiny gold': 2},
    'dotted black': {'dark olive': 4, 'vibrant plum': 6},
}


def test_parse_rule():
    line = example_text.split('\n')[0]
    key = 'light red'
    assert mod.parse_rule(line) == (key, example_rules[key])


def test_read_rules():
    with io.StringIO(example_text) as f:
        rules = mod.read_rules(f)
    assert rules == example_rules


def test_reverse_rules():
    assert mod.reverse_rules(example_rules) == example_parents


def test_find_containers():
    expected = [
        # A bright white bag, which can hold your shiny gold bag directly.
        ('shiny gold', 'bright white'),
        # A muted yellow bag, which can hold your shiny gold bag directly.
        ('shiny gold', 'muted yellow'),
        # A dark orange bag, which can hold bright white and muted yellow bags.
        ('shiny gold', 'bright white', 'dark orange'),
        ('shiny gold', 'muted yellow', 'dark orange'),
        # A light red bag, which can hold bright white and muted yellow bags.
        ('shiny gold', 'bright white', 'light red'),
        ('shiny gold', 'muted yellow', 'light red'),
    ]
    result = list(mod._find_containers(example_parents, ('shiny gold',)))
    assert sorted(result) == sorted(expected)


def test_count_containers():
    assert mod.count_containers(example_rules, 'shiny gold') == 4


def test_count_bags():
    assert mod.count_bags(example_rules, 'shiny gold') == 32


example_2 = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""".strip()


def test_count_bags_example_2():
    with io.StringIO(example_2) as f:
        rules = mod.read_rules(f)
    assert mod.count_bags(rules, 'shiny gold') == 126
