import pytest

import solve


EXAMPLES = (
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
)


def _get_example_ids():
    """ Get test ids for EXAMPLES. """
    return ["ex-{}".format(i + 1) for i in range(len(EXAMPLES))]


def _get_example_t(*idx):
    """ Select fields from EXAMPLES. """
    return [tuple(t[i] for i in idx) for t in EXAMPLES]


@pytest.mark.parametrize(
    "stream, expect",
    _get_example_t(0, 1),
    ids=_get_example_ids(),
)
def test_pt1(stream, expect):
    assert solve.solve_pt1(stream) == expect


@pytest.mark.parametrize(
    "stream, expect",
    _get_example_t(0, 2),
    ids=_get_example_ids(),
)
def test_pt2(stream, expect):
    assert solve.solve_pt2(stream) == expect
