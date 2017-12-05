""" Advent of Code 2017, Day 3 tests """
from spiral import spiral, distance, spiral_sums, find_crossover


def test_spiral():
    gen = spiral()
    assert next(gen) == (0, 0)
    assert next(gen) == (1, 0)
    assert next(gen) == (1, -1)
    assert next(gen) == (0, -1)
    assert next(gen) == (-1, -1)
    assert next(gen) == (-1, 0)


def test_spiral_stop():
    assert len(list(spiral(10))) == 10


def test_distance():
    assert distance(1) == 0
    assert distance(12) == 3
    assert distance(23) == 2
    assert distance(1024) == 31


def test_spiral_sums():
    def _test(n):
        v = 0
        for v in spiral_sums(n):
            pass
        return v

    assert _test(1) == 1
    assert _test(2) == 1
    assert _test(3) == 2
    assert _test(4) == 4
    assert _test(5) == 5
    assert _test(9) == 25
    assert _test(20) == 351


def test_sum_crossover():
    assert find_crossover(100) == 122
    assert find_crossover(122) == 133
    assert find_crossover(800) == 806
