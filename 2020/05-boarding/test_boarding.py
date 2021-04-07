import io

import boarding as mod


example_text = """
FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
""".strip()


examples = [
    # bsp, (row, col), seat_id
    ('FBFBBFFRLR', (44, 5), 357),
    ('BFFFBBFRRR', (70, 7), 567),
    ('FFFBBBFRRR', (14, 7), 119),
    ('BBFFBBFRLL', (102, 4), 820),
]

example_bsp = [t[0] for t in examples]
example_seats = [t[1] for t in examples]
example_ids = [t[2] for t in examples]


def test_read_seats():
    with io.StringIO(example_text) as f:
        assert tuple(mod.read_bsp(f)) == tuple(example_bsp)


def test_get_seat_id():
    for bsp, _, seat_id in examples:
        assert mod.get_seat_id(bsp) == seat_id


def test_get_seat():
    for _, seat_t, seat_id in examples:
        assert mod.get_seat(seat_id) == seat_t
