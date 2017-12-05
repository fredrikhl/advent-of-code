""" Advent of Code 2017, Day 2 tests """
from checksums import parse_spreadsheet, find_divisible, sum_diff, sum_divisible


def test_parse_spreadsheet():
    text = u"""
        5 1 9 5
        7 5       3
        \t 2\t4    6 8
    """
    rows = list(parse_spreadsheet(text))
    assert len(rows) == 3
    assert rows == [
        [5, 1, 9, 5],
        [7, 5, 3],
        [2, 4, 6, 8],
    ]


def test_find_divisible():
    combos = [
        ((5, 9, 2, 8), 4),
        ((9, 4, 7, 3), 3),
        ((3, 8, 6, 5), 2),
    ]
    for numbers, expect in combos:
        assert find_divisible(numbers) == expect


def test_sum_diff():
    text = u"""
        5 1 9 5
        7 5 3
        2 4 6 8
    """
    assert sum_diff(parse_spreadsheet(text)) == 18


def test_sum_divisable():
    text = u"""
        5 9 2 8
        9 4 7 3
        3 8 6 5
    """
    assert sum_divisible(parse_spreadsheet(text)) == 9
