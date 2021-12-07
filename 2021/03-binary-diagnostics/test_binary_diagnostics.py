import io

import binary_diagnostics as testmod


input_text = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".strip()

input_tuples = (
    (0, 0, 1, 0, 0),
    (1, 1, 1, 1, 0),
    (1, 0, 1, 1, 0),
    (1, 0, 1, 1, 1),
    (1, 0, 1, 0, 1),
    (0, 1, 1, 1, 1),
    (0, 0, 1, 1, 1),
    (1, 1, 1, 0, 0),
    (1, 0, 0, 0, 0),
    (1, 1, 0, 0, 1),
    (0, 0, 0, 1, 0),
    (0, 1, 0, 1, 0),
)

expect_pt1 = 198
expect_pt2 = 230


def test_parse_byte():
    assert testmod.parse_byte('10010') == (1, 0, 0, 1, 0)
    assert testmod.parse_byte('10010', bytesize=5) == (1, 0, 0, 1, 0)


def test_read_tuples():
    with io.StringIO(input_text) as f:
        assert tuple(testmod.read_bytes(f)) == input_tuples


def test_get_common():
    assert testmod.get_common(input_tuples, testmod.MOST) == (1, 0, 1, 1, 0)
    assert testmod.get_common(input_tuples, testmod.LEAST) == (0, 1, 0, 0, 1)


def test_match_bytes():
    t = ((0, 0), (0, 1), (1, 0), (1, 1))
    assert testmod.match_bytes(t, 0, 1) == ((1, 0), (1, 1))
    assert testmod.match_bytes(t, 1, 0) == ((0, 0), (1, 0))


def test_reduce_common():
    assert testmod.reduce_common(input_tuples,
                                 testmod.MOST) == (1, 0, 1, 1, 1)
    assert testmod.reduce_common(input_tuples,
                                 testmod.LEAST) == (0, 1, 0, 1, 0)


def test_to_number():
    assert testmod.to_number((1, 0, 1, 1, 0)) == 22
    assert testmod.to_number((0, 1, 0, 0, 1)) == 9
    assert testmod.to_number((1, 0, 1, 1, 1)) == 23
    assert testmod.to_number((0, 1, 0, 1, 0)) == 10


def test_part_1():
    assert testmod.solve_pt1(input_tuples) == expect_pt1


def test_part_2():
    assert testmod.solve_pt2(input_tuples) == expect_pt2
