""" Advent of Code 2017, Day 5 tests """
from memory import cycle, redistribute


def test_cycle():
    assert cycle([0, 2, 7, 0]) == [2, 4, 1, 2]
    assert cycle([2, 4, 1, 2]) == [3, 1, 2, 3]
    assert cycle([3, 1, 2, 3]) == [0, 2, 3, 4]
    assert cycle([0, 2, 3, 4]) == [1, 3, 4, 1]
    assert cycle([1, 3, 4, 1]) == [2, 4, 1, 2]


def test_redistribute_once():
    for total, interval, bank in redistribute([0, 2, 7, 0]):
        pass
    assert total == interval
    assert total == 5
    assert bank == [2, 4, 1, 2]


def test_redistribute_twice():
    for total, interval, bank in redistribute([0, 2, 7, 0], 2):
        pass
    assert interval == 4
    assert bank == [2, 4, 1, 2]
