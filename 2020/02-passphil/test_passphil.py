""" Advent of Code 2020, Day 2 tests """
import io

import passphil as mod


def test_entry_parse():
    entry = mod.parse_entry('21-11 ?: ::cdabcdab$d')
    assert entry == (21, 11, '?', '::cdabcdab$d')


input_text = """
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
""".strip()


entries = (
    mod.entry_t(1, 3, 'a', 'abcde'),
    mod.entry_t(1, 3, 'b', 'cdefg'),
    mod.entry_t(2, 9, 'c', 'ccccccccc'),
)


def test_read_entries():
    with io.StringIO(input_text) as f:
        result = tuple(mod.read_entries(f))
        assert result == entries


valid_count = True, False, True


def test_is_valid_count():
    for entry, expected in zip(entries, valid_count):
        assert mod.is_valid_count(entry) == expected


valid_pos = True, False, False


def test_is_valid_pos():
    for entry, expected in zip(entries, valid_pos):
        assert mod.is_valid_pos(entry) == expected


def test_count_pt1():
    expected = sum(valid_count)
    assert mod.count_valid(entries, mod.is_valid_count) == expected


def test_count_pt2():
    expected = sum(valid_pos)
    assert mod.count_valid(entries, mod.is_valid_pos) == expected
