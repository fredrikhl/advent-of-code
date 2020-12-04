""" Advent of Code 2020, Day 4 tests """
import io

import passproc as mod


example_text = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""


example = (
    {'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd',
     'byr': '1937', 'iyr': '2017', 'cid': '147', 'hgt': '183cm'},
    {'iyr': '2013', 'ecl': 'amb', 'cid': '350', 'eyr': '2023',
     'pid': '028048884', 'hcl': '#cfa07d', 'byr': '1929'},
    {'hcl': '#ae17e1', 'iyr': '2013', 'eyr': '2024', 'ecl': 'brn',
     'pid': '760753108', 'byr': '1931', 'hgt': '179cm'},
    {'hcl': '#cfa07d', 'eyr': '2025', 'pid': '166559648', 'iyr': '2011',
     'ecl': 'brn', 'hgt': '59in'}
)


# part 2 example
valid_passports = (
    {'pid': '087499704', 'hgt': '74in', 'ecl': 'grn', 'iyr': '2012',
     'eyr': '2030', 'byr': '1980', 'hcl': '#623a2f'},
    {'eyr': '2029', 'ecl': 'blu', 'cid': '129', 'byr': '1989', 'iyr': '2014',
     'pid': '896056539', 'hcl': '#a97842', 'hgt': '165cm'},
    {'hcl': '#888785', 'hgt': '164cm', 'byr': '2001', 'iyr': '2015',
     'cid': '88', 'pid': '545766238', 'ecl': 'hzl', 'eyr': '2022'},
    {'iyr': '2010', 'hgt': '158cm', 'hcl': '#b6652a', 'ecl': 'blu',
     'byr': '1944', 'eyr': '2021', 'pid': '093154719'},
)


# part 2 example
invalid_passports = (
    {'eyr': '1972', 'cid': '100', 'hcl': '#18171d', 'ecl': 'amb', 'hgt': '170',
     'pid': '186cm', 'iyr': '2018', 'byr': '1926'},
    {'iyr': '2019', 'hcl': '#602927', 'eyr': '1967', 'hgt': '170cm',
     'ecl': 'grn', 'pid': '012533040', 'byr': '1946'},
    {'hcl': 'dab227', 'iyr': '2012', 'ecl': 'brn', 'hgt': '182cm',
     'pid': '021572410', 'eyr': '2020', 'byr': '1992', 'cid': '277'},
    {'hgt': '59cm', 'ecl': 'zzz', 'eyr': '2038', 'hcl': '74454a',
     'iyr': '2023', 'pid': '3556412378', 'byr': '2007'},
)


def test_parse_line():
    items = (('byr', '1'), ('hcl', '#baz'))
    text = ' '.join(key + ':' + value for key, value in items)
    assert tuple(mod.parse_line(text)) == items


def test_read_passports():
    with io.StringIO(example_text) as f:
        passports = tuple(mod.read_passports(f))
        print(passports)
        assert len(passports) == 4
        assert passports == example


def test_is_complete():
    for p in valid_passports:
        assert mod.is_complete(p)


def test_is_not_complete():
    incomplete = dict(valid_passports[1])
    del incomplete['ecl']
    assert not mod.is_complete(incomplete)


def test_count_complete():
    assert mod.count_passports(example, mod.is_complete) == 2


def test_int_validator():
    minval, maxval = 10, 15
    is_valid = mod.get_int_validator(minval, maxval)

    assert is_valid(str(minval))
    assert is_valid(str(maxval))
    assert not is_valid(str(minval - 1))
    assert not is_valid(str(maxval + 1))
    assert not is_valid(str())
    assert not is_valid('non-digits123')


def test_byr():
    is_valid = mod.VALIDATORS['byr']
    assert is_valid('2002')
    assert not is_valid('2003')


def test_hgt():
    is_valid = mod.VALIDATORS['hgt']
    assert is_valid('60in')
    assert is_valid('190cm')
    assert not is_valid('190in')
    assert not is_valid('190')


def test_hcl():
    is_valid = mod.VALIDATORS['hcl']
    assert is_valid('#123abc')
    assert not is_valid('#123abz')
    assert not is_valid('123abc')


def test_ecl():
    is_valid = mod.VALIDATORS['ecl']
    assert is_valid('brn')
    assert not is_valid('wat')


def test_pid():
    is_valid = mod.VALIDATORS['pid']
    assert is_valid('000000001')
    assert not is_valid('0123456789')


def test_is_valid():
    for p in valid_passports:
        assert mod.is_valid(p)


def test_is_not_valid():
    for p in invalid_passports:
        assert not mod.is_valid(p)


def test_count_valid():
    passports = valid_passports + invalid_passports
    assert mod.count_passports(passports, mod.is_valid) == len(valid_passports)
