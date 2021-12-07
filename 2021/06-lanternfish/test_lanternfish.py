import io
import pytest
import lanternfish as mod


input_text = "3,4,3,1,2"
expected_state = (
    (3, 4, 3, 1, 2),
    (2, 3, 2, 0, 1),
    (1, 2, 1, 6, 0, 8),
    (0, 1, 0, 5, 6, 7, 8),
)
input_vals = expected_state[0]


def test_read_counts():
    with io.StringIO(input_text) as f:
        assert tuple(mod.read_counts(f)) == input_vals


def test_new_state():
    numbers = (2,) + 3 * (4,) + 5 * (6,) + 7 * (8,)
    expect = (0, 0, 1, 0, 3, 0, 5, 0, 7)
    assert tuple(mod.new_state(numbers)) == expect


@pytest.mark.parametrize('i', range(len(expected_state) - 1))
def test_next_state(i):
    state = mod.new_state(expected_state[i])
    expected = mod.new_state(expected_state[i + 1])
    assert mod.next_state(state) == expected


@pytest.mark.parametrize('i', range(len(expected_state)))
def test_get_state(i):
    expected = mod.new_state(expected_state[i])
    assert mod.get_state(input_vals, i) == expected


def test_part_1():
    assert mod.solve_pt1(input_vals) == 5934


def test_part_2():
    assert mod.solve_pt2(input_vals) == 26984457539
