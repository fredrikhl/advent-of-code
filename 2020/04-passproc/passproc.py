"""
AoC Day 4: Passport Processing
"""
import re
import os
import sys


VALID_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
REQUIRED_FIELDS = VALID_FIELDS - {'cid'}


def get_int_validator(minval, maxval):

    def validate_int(value):
        if not value.isdigit():
            return False

        return minval <= int(value) <= maxval

    return validate_int


HCL_REGEX = re.compile('^#[0-9a-f]{6}$')
ECL_VALUES = set('amb blu brn gry grn hzl oth'.split())
HGT_UNITS = {
    'cm': get_int_validator(150, 193),
    'in': get_int_validator(59, 76),
}


def validate_hgt(raw_value):
    value, unit = raw_value[:-2], raw_value[-2:]

    if unit not in HGT_UNITS:
        return False

    return HGT_UNITS[unit](value)


VALIDATORS = {
    'byr': get_int_validator(1920, 2002),
    'iyr': get_int_validator(2010, 2020),
    'eyr': get_int_validator(2020, 2030),
    'hgt': validate_hgt,
    'hcl': lambda v: bool(HCL_REGEX.match(v)),
    'ecl': lambda v: v in ECL_VALUES,
    'pid': lambda v: len(v) == 9 and v.isdigit(),
}


def parse_line(text):
    """ split line into key-value pairs. """
    items = text.split()
    for item in items:
        key, sep, value = item.partition(':')
        if not sep:
            raise ValueError('invalid format %r (%r)' % (item, text))
        if key not in VALID_FIELDS:
            raise ValueError('unknown field %r (%r)' % (key, text))
        yield key, value


def read_passports(fd):
    """ read and parse passport dicts from a file-like object. """
    current = {}
    for lineno, line in enumerate(fd, 1):
        if not line.strip():
            if current:
                yield current
            current = {}
            continue

        try:
            current.update(parse_line(line.strip()))
        except Exception as e:
            raise ValueError('error on line %d (%r): %s' % (lineno, line, e))

    if current:
        yield current


def is_complete(passport):
    """ check if passport contains required fields. """
    return not (REQUIRED_FIELDS - set(passport))


def is_valid(passport):
    """ check if passport fields are valid. """
    if not is_complete(passport):
        return False
    return all(field in passport and validate(passport[field])
               for field, validate in VALIDATORS.items())


def count_passports(passports, filter_cb):
    """ count valid passports according to callback. """
    return sum(filter_cb(p) for p in passports)


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        passports = tuple(read_passports(f))
    print('Total: {} passports'.format(len(passports)))

    num_complete = count_passports(passports, is_complete)
    print(f'Part 1: {num_complete} complete passports')

    num_valid = count_passports(passports, is_valid)
    print(f'Part 2: {num_valid} valid passports')


if __name__ == '__main__':
    main()
