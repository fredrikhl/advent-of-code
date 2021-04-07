""" Advent of Code 2020, Day 3 tests """
import io

import trajectory as mod


# Tree, Square
X, _ = mod.TREE, mod.SQUARE

example_text = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip()

example = (
    (_, _, X, X, _, _, _, _, _, _, _),
    (X, _, _, _, X, _, _, _, X, _, _),
    (_, X, _, _, _, _, X, _, _, X, _),
    (_, _, X, _, X, _, _, _, X, _, X),
    (_, X, _, _, _, X, X, _, _, X, _),
    (_, _, X, _, X, X, _, _, _, _, _),
    (_, X, _, X, _, X, _, _, _, _, X),
    (_, X, _, _, _, _, _, _, _, _, X),
    (X, _, X, X, _, _, _, X, _, _, _),
    (X, _, _, _, X, X, _, _, _, _, X),
    (_, X, _, _, X, _, _, _, X, _, X),
)

slope_counts = [
    ((1, 1), 2),
    ((3, 1), 7),
    ((5, 1), 3),
    ((7, 1), 4),
    ((1, 2), 2),
]


def generate_matrix(cols, rows, pattern=(_, X)):
    return tuple(
        tuple(pattern[(c + r * c) % len(pattern)] for c in range(cols))
        for r in range(rows))


def test_parse_row():
    text = example_text.split()[0]
    expect = example[0]
    assert tuple(mod.parse_row(text)) == expect


def test_read_rows():
    with io.StringIO(example_text) as f:
        assert tuple(mod.read_rows(f)) == example


def test_move():
    m = generate_matrix(5, 5)
    t = (3, 2)
    assert mod.move(m, (0, 0), t) == t


def test_move_oob():
    """ move out of bounds (col should wrap, row should not) """
    cols, rows = (11, 11)
    m = generate_matrix(cols, rows)
    corner = (cols - 1, rows - 1)
    assert mod.move(m, corner, (1, 1)) == (0, rows)


def test_generate_path():
    rows, cols = (10, 5)
    m = generate_matrix(cols, rows)
    path = tuple(mod.generate_path(m, (0, 0), (1, 1)))
    assert path[0] == (0, 0)
    assert path[cols] == (0, cols)
    assert path[-1] == (cols - 1 % rows, rows - 1)


def test_is_tree():
    m = generate_matrix(3, 4)
    for rownum, row in enumerate(m):
        for colnum, value in enumerate(row):
            assert mod.is_tree(m, (colnum, rownum)) is (value == X)


def test_count_trees():
    for slope, trees in slope_counts:
        assert mod.count_trees(example, slope) == trees


def test_solve_product():
    slopes = [s for s, _ in slope_counts]
    assert mod.solve_product(example, slopes) == 336
