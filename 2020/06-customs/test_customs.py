import io

import customs as mod

example_text = """
abc

a
b
c

ab
ac

a
a
a
a

b
""".strip()

example = (
    ({'a', 'b', 'c'},),
    ({'a'}, {'b'}, {'c'}),
    ({'a', 'b'}, {'a', 'c'}),
    ({'a'}, {'a'}, {'a'}, {'a'}),
    ({'b'},),
)


def test_read_groups():
    with io.StringIO(example_text) as f:
        assert tuple(mod.read_groups(f)) == example


def test_any_yes():
    expected = (3, 3, 3, 1, 1)
    for group, count in zip(example, expected):
        assert len(mod.any_yes(group)) == count


def test_all_yes():
    expected = (3, 0, 1, 1, 1)
    for group, count in zip(example, expected):
        assert len(mod.all_yes(group)) == count


def test_sum_any():
    assert mod.sum_groups(example, mod.any_yes) == 11


def test_sum_all():
    assert mod.sum_groups(example, mod.all_yes) == 6
