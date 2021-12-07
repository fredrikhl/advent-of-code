import io

import sonar_sweep as testmod


input_text = """
199
200
208
210
200
207
240
269
260
263
""".strip()
input_numbers = (199, 200, 208, 210, 200, 207, 240, 269, 260, 263)
expect_pt1 = 7
expect_pt2 = 5


def test_read_numbers():
    with io.StringIO(input_text) as f:
        assert tuple(testmod.read_numbers(f)) == input_numbers


def test_get_deltas():
    numbers = (1, 2, 3, 2, 1, 2)
    deltas = (1, 1, -1, -1, 1)
    assert tuple(testmod.get_deltas(numbers)) == deltas


def test_count_incr():
    numbers = (1, 2, 3, 2, 1, 2)
    n_inc = sum((True, True, False, False, True))
    assert testmod.count_incr(numbers) == n_inc


def test_part_1():
    assert testmod.solve_pt1(input_numbers) == expect_pt1


def test_sliding_window_2():
    numbers = (1, 2, 3, 4, 5)
    pairs = ((1, 2), (2, 3), (3, 4), (4, 5))
    assert tuple(testmod.sliding_window(numbers, 2)) == pairs


def test_sliding_window_3():
    numbers = (1, 2, 3, 4, 5)
    trips = ((1, 2, 3), (2, 3, 4), (3, 4, 5))
    assert tuple(testmod.sliding_window(numbers, 3)) == trips


def test_sliding_sums_3():
    numbers = (1, 2, 3, 4, 5)
    sums = (6, 9, 12)
    assert tuple(testmod.sliding_sums(numbers, 3)) == sums


def test_part_2():
    assert testmod.solve_pt2(input_numbers) == expect_pt2
