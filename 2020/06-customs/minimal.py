from functools import reduce
from os.path import join as pj, dirname


with open(pj(dirname(__file__), 'input.txt')) as f:
    groups = [
        [set(i) for i in group.split('\n') if i]
        for group in f.read().split('\n\n')]

print('Part 1:', sum(len(reduce(set.union, g)) for g in groups))
print('Part 2:', sum(len(reduce(set.intersection, g)) for g in groups))
