import io

import dive as testmod


input_text = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".strip()
input_deltas = ((5, 0), (0, 5), (8, 0), (0, -3), (0, 8), (2, 0))
expect_pt1 = 150
expect_pt2 = 900


def test_parse_op():
    assert testmod.parse_op('forward 0') == (0, 0)
    assert testmod.parse_op('forward 2') == (2, 0)
    assert testmod.parse_op('up 3') == (0, -3)
    assert testmod.parse_op('up -3') == (0, 3)
    assert testmod.parse_op('down 0123') == (0, 123)


def test_read_ops():
    with io.StringIO(input_text) as f:
        assert tuple(testmod.read_ops(f)) == input_deltas


def test_next_pos():
    assert testmod.next_pos((0, 0), (5, 0)) == (5, 0)
    assert testmod.next_pos((5, 0), (0, 5)) == (5, 5)
    assert testmod.next_pos((5, 5), (8, 0)) == (13, 5)


def test_next_aim():
    assert testmod.next_aim((0, 0, 0), (5, 0)) == (5, 0, 0)
    assert testmod.next_aim((5, 0, 0), (0, 5)) == (5, 5, 0)
    assert testmod.next_aim((5, 5, 0), (8, 0)) == (13, 5, 40)


def test_part_1():
    assert testmod.solve_pt1(input_deltas) == expect_pt1


def test_part_2():
    assert testmod.solve_pt2(input_deltas) == expect_pt2
