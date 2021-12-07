import io

import crab_sort as mod


input_text = "16,1,2,0,4,2,7,1,2,14"
input_nums = (16, 1, 2, 0, 4, 2, 7, 1, 2, 14)


def test_read_state():
    with io.StringIO(input_text) as f:
        assert tuple(mod.read_state(f)) == input_nums


def test_part_1():
    assert mod.solve_pt1(input_nums) == 37


def test_part_2():
    assert mod.solve_pt2(input_nums) == 168
