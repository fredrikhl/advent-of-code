import io

import shuttle as mod


example_text = """
939
7,13,x,x,59,x,31,19
""".strip()

target = 939
buses = (7, 13, None, None, 59, None, 31, 19)


def test_parse_file():
    with io.StringIO(example_text) as f:
        assert mod.parse_file(f) == (target, buses)


def test_get_wait():
    assert mod.get_wait(100, 10) == 0
    assert mod.get_wait(101, 10) == 9
    assert mod.get_wait(99, 10) == 1
    assert mod.get_wait(53, 7) == 3


def test_find_first():
    assert mod.find_first_available(buses, target) == 59


def test_solve_next():
    assert mod.solve_next_bus(buses, target) == 295


def test_solve_contest():
    assert mod.solve_contest(buses, target) == 1068781
