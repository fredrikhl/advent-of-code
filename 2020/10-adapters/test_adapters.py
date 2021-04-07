import io

import adapters as mod


example = (16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4)
example_b = (28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
             38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3)


def test_read_file():
    for numbers in (example, example_b):
        with io.StringIO('\n'.join(map(str, numbers))) as f:
            assert tuple(mod.read_numbers(f)) == numbers


all_jumps = (
    # The charging outlet ... an adapter rated 1 jolt (difference of 1).
    1,
    # From your 1-jolt ... is your 4-jolt rated adapter (difference of 3).
    3,
    # From the 4-jolt ... pick the adapter rated 5 jolts (difference of 1).
    1,
    # ... next choices ... 6 and then ... 7 (with difference of 1 and 1).
    1, 1,
    # The only adapter ... is the one rated 10 jolts (difference of 3).
    3,
    # From 10, ... choose 11 (difference of 1) and then 12 (difference of 1).
    1, 1,
    # After 12, ... rating of 15 (difference of 3), then 16 (difference of 1),
    # then 19 (difference of 3).
    3, 1, 3,
    # Finally, ... rating is 22 jolts (always a difference of 3).
    3,
)


def test_find_all_jumps():
    assert tuple(mod.find_all_jumps(example)) == all_jumps


def test_solve_score():
    assert mod.solve_score(example) == 35
    assert mod.solve_score(example_b) == 220


next_jumps = (
    (0, (1,)),
    (1, (4,)),
    (4, (5, 6, 7)),
    (5, (6, 7)),
    (6, (7,)),
    (7, (10,)),
    (10, (11, 12)),
    (11, (12,)),
    (12, (15,)),
    (15, (16,)),
    (16, (19,)),
    (19, (22,)),
)


def test_gen_jump_table():
    jumps = tuple(mod.gen_jump_table(example))
    assert jumps == next_jumps


def test_count_combinations():
    assert mod.count_combinations(example) == 8
    assert mod.count_combinations(example_b) == 19208
