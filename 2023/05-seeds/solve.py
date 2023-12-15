"""
Advent of Code 2023

`Day 5 <https://adventofcode.com/2023/day/5>`_:
If You Give A Seed A Fertilizer
"""
import os
import re
import sys


RE_SEEDS = re.compile(r"seeds: (.*)")
RE_MAP = re.compile(r"(\w+)-to-(\w+) map:")
RE_NUMS = re.compile(r"\d+")


def parse_numbers(value, n=None):
    """ Get numbers from string. """
    numbers = tuple(int(n) for n in RE_NUMS.findall(value))
    if n and len(numbers) != n:
        raise ValueError("expected %d numbers (got %d)" % (n, len(numbers)))
    return numbers


def read_params(fd):
    """ Read seeds and maps from file-like *fd*. """
    key = None
    seen = set()
    for lineno, raw_line in enumerate(fd, 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            m = RE_SEEDS.match(line)
            if m:
                if "seeds" in seen:
                    raise ValueError("duplicate seeds entry")
                seen.add("seeds")
                yield "seeds", parse_numbers(m.group(1))
                continue

            m = RE_MAP.match(line)
            if m:
                key = m.groups()
                if key in seen:
                    raise ValueError("duplicate map entry: %s-to-%s" % key)
                seen.add(key)
                yield "map", key
                continue

            if key:
                yield key, parse_numbers(line, 3)
                continue

            raise ValueError("unknown content")
        except Exception as e:
            raise ValueError("Invalid card on line %d: %s (%s)"
                             % (lineno, repr(line), e))


class RangeMap(object):
    """ A number range mapper. """

    def __init__(self, f, t, n):
        self._f = f
        self._t = t
        self._n = n

    def __repr__(self):
        return "RangeMap({}, {}, {})".format(self._f, self._t, self._n)

    def __contains__(self, number):
        if number >= self._f and number < self._f + self._n:
            return True
        return False

    def __getitem__(self, number):
        if number not in self:
            return IndexError("out of range: " + repr(number))
        return self._t + (number - self._f)

    @classmethod
    def from_string(cls, value):
        """ Get RangeMap from string with three numbers. """
        t, f, n = parse_numbers(value, 3)
        return cls(f, t, n)


def build_maps(items):
    seeds = None
    source_to_dest = Map()
    for key, value in items:
        if key == "seeds":
            if seeds is None:
                seeds = value
            else:
                raise ValueError("duplicate seeds")
            continue

        if key == "map":
            src_key, dst_key = value
            source_to_dest.add_source(src_key, dst_key)
            continue

        src, dst = key
        t, f, n = value
        source_to_dest.add_range(src, dst, t, f, n)
        continue

    source_to_dest.validate_sources()
    return seeds, source_to_dest


class Map(object):
    """ Map source point to location point or vice versa. """

    # This is messy and pretty inefficient.  Solving both the example and input
    # amppings for part 1 + 2 takes ~ 3 minutes.
    #
    # The *proper* solution is probably to cut out all the intermediary
    # mappings, and map directly from seed to location.  E.g. turn:
    #
    #   a-b: 0-49 -> 50-99, 50-99 -> 0-49
    #   b-c: 0-49 -> 50-99, 50-99 -> 0-49
    #
    # into:
    #
    #   a-c: 0-99 -> 0-99

    def __init__(self):
        self._src_to_dst = {}
        self._dst_to_src = {}
        self._range_maps_to = {}
        self._range_maps_from = {}

    def add_source(self, source, dest):
        if source in self._src_to_dst:
            raise ValueError("duplicate source key: " + repr(source))
        if dest in self._src_to_dst:
            raise ValueError("duplicate dest key: " + repr(dest))
        self._src_to_dst[source] = dest
        self._dst_to_src[dest] = source

    def add_range(self, source, dest, t, f, n):
        if source not in self._src_to_dst:
            raise ValueError("unknown source: " + repr(source))
        self._range_maps_to.setdefault(
            (source, dest), []).append(RangeMap(f, t, n))
        self._range_maps_from.setdefault(
            (dest, source), []).append(RangeMap(t, f, n))

    def validate_sources(self):
        for v in self._src_to_dst.values():
            if v == "location":
                # target location, has no mapping
                continue
            if v not in self._src_to_dst:
                raise ValueError("no mapping for: " + repr(v))
        if "seed" not in self._src_to_dst:
            raise ValueError("no mapping for: " + repr("seed"))

        for v in self._dst_to_src.values():
            if v == "seed":
                # target location, has no mapping
                continue
            if v not in self._dst_to_src:
                raise ValueError("no mapping for: " + repr(v))
        if "location" not in self._dst_to_src:
            raise ValueError("no mapping for: " + repr("location"))

    def lookup_seed(self, value):
        source = "seed"
        dest = source
        while source in self._src_to_dst:
            dest = self._src_to_dst[source]
            # print("step", source, dest, value)
            key = source, dest
            for rm in self._range_maps_to[key]:
                if value in rm:
                    value = rm[value]
                    source = dest
                    break
            else:
                # unmapped value
                source = dest
        return dest, value

    def lookup_location(self, value):
        source = "location"
        dest = source
        while source in self._dst_to_src:
            dest = self._dst_to_src[source]
            # print("step", source, dest, value)
            key = source, dest
            for rm in self._range_maps_from[key]:
                if value in rm:
                    value = rm[value]
                    source = dest
                    break
            else:
                # unmapped value
                source = dest
        return dest, value


def pairs(iterable):
    args = [iter(iterable)] * 2
    return zip(*args, strict=True)


def solve_pt1(params):
    seeds, source_to_dest = build_maps(params)
    return min(value for _, value in (source_to_dest.lookup_seed(s)
                                      for s in seeds))


def solve_pt2(params):
    seeds, source_to_dest = build_maps(params)

    seed_ranges = []
    for start, size in pairs(seeds):
        seed_ranges.append(RangeMap(start, 0, size))

    i = 0
    while True:
        _, value = source_to_dest.lookup_location(i)
        for rm in seed_ranges:
            if value in rm:
                return i
        else:
            i += 1
            continue


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main():
    files = sys.argv[1:] or [default_input_file]

    for i, filename in enumerate(files):
        print(bool(i) * '\n' + 'Solutions for', filename)
        with open(filename) as f:
            params = list(read_params(f))

        pt1 = solve_pt1(params)
        print('Part 1:', pt1)

        pt2 = solve_pt2(params)
        print('Part 2:', pt2)


if __name__ == '__main__':
    main()
