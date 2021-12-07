import io

import hydrothermal as mod


input_text = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip()

input_tuples = (
    ((0, 9), (5, 9)),
    ((8, 0), (0, 8)),
    ((9, 4), (3, 4)),
    ((2, 2), (2, 1)),
    ((7, 0), (7, 4)),
    ((6, 4), (2, 0)),
    ((0, 9), (2, 9)),
    ((3, 4), (1, 4)),
    ((0, 0), (8, 8)),
    ((5, 5), (8, 2)),
)


def test_parse_point():
    assert mod.parse_point('0,9') == (0, 9)
    assert mod.parse_point('5,9') == (5, 9)


def test_parse_line():
    assert mod.parse_line('0,9 -> 5,9') == ((0, 9), (5, 9))


def test_read_lines():
    with io.StringIO(input_text) as f:
        assert tuple(mod.read_lines(f)) == input_tuples


def test_iter_line_v():
    line = ((1, 1), (1, 3))
    assert tuple(mod.iter_points(line)) == ((1, 1), (1, 2), (1, 3))


def test_iter_line_h():
    line = ((9, 7), (7, 7))
    assert tuple(mod.iter_points(line)) == ((9, 7), (8, 7), (7, 7))


def test_iter_line_d():
    line_a = ((1, 1), (3, 3))
    assert tuple(mod.iter_points(line_a)) == ((1, 1), (2, 2), (3, 3))
    line_b = ((9, 7), (7, 9))
    assert tuple(mod.iter_points(line_b)) == ((9, 7), (8, 8), (7, 9))


def test_part_1():
    assert mod.solve_pt1(input_tuples) == 5


def test_part_2():
    assert mod.solve_pt2(input_tuples) == 12
