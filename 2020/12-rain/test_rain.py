import io

import rain as mod


example_text = """
F10
N3
F7
R90
F11
""".strip()

example = (('F', 10), ('N', 3), ('F', 7), ('R', 90), ('F', 11))


def test_parse_line():
    assert mod.parse_line('R90') == ('R', 90)
    assert mod.parse_line('N3') == ('N', 3)


def test_parse_file():
    with io.StringIO(example_text) as f:
        assert tuple(mod.parse_file(f)) == example


def test_move():
    assert mod.move((10, 0), ('N', 3)) == (10, 3)


def test_move_state():
    assert mod.move((0, 0, 'E'), ('N', 10)) == (0, 10, 'E')


def test_turn():
    assert mod.turn((0, 0, 'E'), ('R', 90)) == (0, 0, 'S')
    assert mod.turn((1, -1, 'E'), ('R', 180)) == (1, -1, 'W')
    assert mod.turn((1, -1, 'E'), ('R', 270)) == (1, -1, 'N')
    assert mod.turn((1, -1, 'E'), ('L', 270)) == (1, -1, 'S')


def test_rotate():
    assert mod.rotate((10, 4), ('R', 90)) == (4, -10)
    assert mod.rotate((10, 4), ('L', 90)) == (-4, 10)
    assert mod.rotate((10, 4), ('L', 270)) == (4, -10)


def test_follow():
    assert mod.follow((0, 0, 'E'), ('F', 10)) == (10, 0, 'E')
    assert mod.follow((10, 3, 'E'), ('F', 7)) == (17, 3, 'E')
    assert mod.follow((17, 3, 'S'), ('F', 11)) == (17, -8, 'S')


def test_towards():
    assert mod.towards((0, 0), (10, 1), ('F', 10)) == (100, 10)
    assert mod.towards((100, 10), (10, 4), ('F', 7)) == (170, 38)
    assert mod.towards((170, 38), (4, -10), ('F', 11)) == (214, -72)


def test_travel_state():
    assert mod.travel_state((0, 0, 'E'), example) == (17, -8, 'S')


def test_travel_waypoint():
    assert mod.travel_waypoint((0, 0), (10, 1), example) == ((214, -72),
                                                             (4, -10))


def test_distance():
    assert mod.distance((17, -8)) == 25
    assert mod.distance((214, -72)) == 286
