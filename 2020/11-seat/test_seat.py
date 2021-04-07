import io

import seat as mod


# Tree, Square
_, L, X = mod.FLOOR, mod.EMPTY, mod.TAKEN


example_text = """
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
""".strip()


example_init = (
    (L, _, L, L, _, L, L, _, L, L),
    (L, L, L, L, L, L, L, _, L, L),
    (L, _, L, _, L, _, _, L, _, _),
    (L, L, L, L, _, L, L, _, L, L),
    (L, _, L, L, _, L, L, _, L, L),
    (L, _, L, L, L, L, L, _, L, L),
    (_, _, L, _, L, _, _, _, _, _),
    (L, L, L, L, L, L, L, L, L, L),
    (L, _, L, L, L, L, L, L, _, L),
    (L, _, L, L, L, L, L, _, L, L),
)

example = (
    (X, _, X, L, _, L, X, _, X, X),
    (X, L, L, L, X, L, L, _, L, X),
    (L, _, X, _, L, _, _, X, _, _),
    (X, L, X, X, _, X, X, _, L, X),
    (X, _, X, L, _, L, L, _, L, L),
    (X, _, X, L, X, L, X, _, X, X),
    (_, _, L, _, L, _, _, _, _, _),
    (X, L, X, L, X, X, L, X, L, X),
    (X, _, L, L, L, L, L, L, _, L),
    (X, _, X, L, X, L, X, _, X, X),
)


def generate_matrix(cols, rows, pattern=(_, L, X)):
    return tuple(
        tuple(pattern[(c + r * cols) % len(pattern)] for c in range(cols))
        for r in range(rows))


def test_parse_row():
    text = example_text.split()[0]
    expect = example[0]
    assert tuple(mod.parse_row(text)) == expect


def test_read_rows():
    with io.StringIO(example_text) as f:
        assert tuple(mod.read_rows(f)) == example


def test_iter_matrix():
    m = generate_matrix(3, 3)
    assert len(tuple(mod.iter_matrix(m))) == 3 * 3


def test_count_seats():
    m = generate_matrix(6, 2, pattern=(X, X, X, L, L, _))
    assert mod.count_seats(m, X) == 6
    assert mod.count_seats(m, L) == 4
    assert mod.count_seats(m, _) == 2


def test_count_taken():
    assert mod.count_seats(example, X) == 37


def test_get_adjacent():
    m = generate_matrix(3, 3)

    expect = (
        ((0, 0), [(0, 1), (1, 0), (1, 1)]),
        ((2, 2), [(2, 1), (1, 2), (1, 1)]),
        ((1, 1), [(1, 2), (1, 0), (2, 1), (0, 1),
                  (2, 2), (0, 0), (0, 2), (2, 0)])
    )

    for position, adjacent in expect:
        assert mod.get_kernel(m, position, True) == set(adjacent)


def test_get_visible():
    m = generate_matrix(5, 5, pattern=(_,))

    pos = (2, 2)
    corners = (0, 0), (4, 4), (4, 0), (0, 4)
    edges = (0, 2), (2, 0), (4, 2), (2, 4)

    assert mod.get_kernel(m, pos, False) == set(corners + edges)


minimal = (
    (_, X, _, _, _),
    (X, X, L, _, L),
    (X, X, L, L, _),
    (X, _, _, L, _),
    (_, _, _, X, _),
)


def test_next_value_adjacent():
    tests = (
        (1, 3, _, _),  # floor -> floor
        (0, 3, X, X),  # taken -> taken
        (1, 2, X, L),  # taken -> empty
        (2, 2, L, L),  # empty -> empty
        (3, 2, L, X),  # empty -> taken
    )
    for col, row, val, expect in tests:
        print(col, row, val, expect)
        assert minimal[row][col] == val
        assert mod.next_value(minimal, (col, row), False) == expect


def test_next_value_visible():
    tests = (
        (1, 3, _, _),  # floor -> floor
        (0, 2, X, X),  # taken -> taken
        (1, 2, X, L),  # taken -> empty
        (2, 2, L, L),  # empty -> empty
        (3, 2, L, X),  # empty -> taken
    )

    for col, row, val, expect in tests:
        print(col, row, val, expect)
        assert minimal[row][col] == val
        assert mod.next_value(minimal, (col, row), True) == expect


def test_get_changes_adjacent():
    expected = ((0, 1, L), (1, 1, L), (4, 1, X),
                (0, 2, L), (1, 2, L), (3, 2, X))
    assert tuple(mod.get_changes(minimal, False)) == expected


def test_get_changes_visible():
    expected = ((4, 1, X), (1, 2, L), (3, 2, X))
    assert tuple(mod.get_changes(minimal, True)) == expected


def test_get_changes_final():
    assert tuple(mod.get_changes(example, False)) == ()


def test_solve_adjacent():
    assert mod.solve(example_init, False) == example


def test_solve_visible():
    assert mod.count_seats(mod.solve(example_init, True), X) == 26
