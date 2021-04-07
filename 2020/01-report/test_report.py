""" Advent of Code 2020, Day 1 tests """
import io

import report as mod


input_text = """
1721
979
366
299
675
1456
""".strip()


numbers = (1721, 979, 366, 299, 675, 1456)
target_sum = 2020
expected = (
    # n, numbers, product
    (2, (1721, 299), 514579),
    (3, (979, 366, 675), 241861950),
)


def test_read_numbers():
    with io.StringIO(input_text) as f:
        assert tuple(mod.read_numbers(f)) == numbers


def test_mul():
    assert mod.mul(2, 3) == 6
    assert mod.mul(1, 2, 3, 4) == 24
    assert mod.mul(1, 2, 3, 4, 0) == 0


def test_find_combo():
    for n, nums, product in expected:
        result = mod.find_combo(numbers, target_sum, n)
        assert sorted(result) == sorted(nums)


def test_solve():
    for n, nums, product in expected:
        r_nums, r_product = mod.solve(numbers, target_sum, n)
        assert sorted(r_nums) == sorted(nums)
        assert r_product == product
