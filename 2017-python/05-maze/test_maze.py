""" Advent of Code 2017, Day 5 tests """
from maze import run, count_steps, part_1_modifier, part_2_modifier


def test_part_1():
    assert part_1_modifier(1) == 2
    assert part_1_modifier(5) == 6


def test_part_2():
    assert part_2_modifier(0) == 1
    assert part_2_modifier(2) == 3
    assert part_2_modifier(3) == 2
    assert part_2_modifier(4) == 3


def test_run():
    simple = [1, 1, 1]
    copy = simple[:]
    runner = run(copy)

    # first step, index 0, jump one ahead (to 1)
    assert next(runner) == (0, 1)

    # second step, index 1, jump one ahead (to 2)
    assert next(runner) == (1, 1)

    # One instruction left: index 2, jump one ahead (done)
    assert list(runner) == [(2, 1), ]

    # The program should not have been modified
    assert simple == copy


def test_run_part_1():
    example = [0, 3, 0, 1, -3]
    runner = run(example, part_1_modifier)

    # First step
    assert next(runner) == (0, 0)
    assert example == [1, 3, 0, 1, -3]

    # Second step
    assert next(runner) == (0, 1)
    assert example == [2, 3, 0, 1, -3]

    # third step
    assert next(runner) == (1, 3)
    assert example == [2, 4, 0, 1, -3]

    # fourth step
    assert next(runner) == (4, -3)
    assert example == [2, 4, 0, 1, -2]

    # fifth, and final step
    assert next(runner) == (1, 4)
    assert example == [2, 5, 0, 1, -2]

    # there should not be any other operations at this point
    assert list(runner) == []


def test_run_part_2():
    example = [0, 3, 0, 1, -3]
    runner = run(example, part_2_modifier)

    assert count_steps(runner) == 10
    assert example == [2, 3, 2, 3, -1]
