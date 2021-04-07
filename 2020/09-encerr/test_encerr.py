import io

import encerr as mod

values = (35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102,
          117, 150, 182, 127, 219, 299, 277, 309, 576)
preamble = 5

invalid = 127
xmas_range = (15, 25, 47, 40)
weakness = 62


def test_read_file():
    with io.StringIO('\n'.join(map(str, values))) as f:
        assert tuple(mod.read_numbers(f)) == values


def test_get_valid():
    assert mod.get_valid((1, 2, 3)) == set((1 + 2, 1 + 3, 2 + 3))


def test_iter_contiguous():
    ranges = tuple(mod.iter_contiguous(values, preamble))
    assert ranges[0] == values[:preamble]
    assert ranges[1] == values[1:1+preamble]
    assert ranges[-1] == values[-preamble:]


def test_get_invalid_values():
    results = mod.get_invalid_values(values, preamble)
    assert next(results) == invalid


def test_find_range():
    assert mod.find_range(values, invalid) == xmas_range


def test_get_weakness():
    assert mod.get_weakness(xmas_range) == weakness
