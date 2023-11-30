""" Advent of Code 2016, Day 4 tests """
import io

import pytest

import checksum as mod


examples = (
    {
        'input': "aaaaa-bbb-z-y-x-123[abxyz]",
        'tuple': ("aaaaa-bbb-z-y-x", 123, "abxyz"),
        'valid': True,
    },
    {
        'input': "a-b-c-d-e-f-g-h-987[abcde]",
        'tuple': ("a-b-c-d-e-f-g-h", 987, "abcde"),
        'valid': True,
    },
    {
        'input': "not-a-real-room-404[oarel]",
        'tuple': ("not-a-real-room", 404, "oarel"),
        'valid': True,
    },
    {
        'input': "totally-real-room-200[decoy]",
        'tuple': ("totally-real-room", 200, "decoy"),
        'valid': False,
    },
)


def get_example_names():
    """ get a test-id for each set of parameters in *examples* """
    return tuple(i['tuple'][0] for i in examples)


def get_example_fields(*fields):
    """ get the given fields for each set of parameters in *examples* """
    if len(fields) == 1:
        return tuple(i[fields[0]] for i in examples)
    else:
        return tuple(tuple(i[f] for f in fields) for i in examples)


@pytest.mark.parametrize(
    "line, room_t",
    get_example_fields("input", "tuple"),
    ids=get_example_names(),
)
def test_parse_room(line, room_t):
    assert mod.parse_room_id(line) == room_t


def test_read_room_file():
    lines = "\n".join(get_example_fields("input"))
    tuples = get_example_fields("tuple")
    with io.StringIO(lines) as f:
        assert tuple(mod.read_room_file(f)) == tuples


@pytest.mark.parametrize(
    "room_t, is_valid",
    get_example_fields("tuple", "valid"),
    ids=get_example_names(),
)
def test_checksum(room_t, is_valid):
    room_id, _, checksum = room_t
    assert (mod.checksum(room_id) == checksum) is is_valid


def test_decrypt():
    assert mod.decrypt("qzmt-zixmtkozy-ivhz", 343) == "very encrypted name"
