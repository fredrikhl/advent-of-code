""" Advent of Code 2017, Day 1 tests """
from captcha import offset_summer, divisible_offset_summer


def test_offset_summer():
    assert offset_summer(1, 1122) == 3
    assert offset_summer(1, 1111) == 4
    assert offset_summer(1, 1234) == 0
    assert offset_summer(1, 91212129) == 9


def test_divisible_offset_summer():
    divisible_offset_summer(2, 1212) == 6
    divisible_offset_summer(2, 1221) == 0
    divisible_offset_summer(2, 123425) == 4
    divisible_offset_summer(2, 123123) == 12
    divisible_offset_summer(2, 12131415) == 4
