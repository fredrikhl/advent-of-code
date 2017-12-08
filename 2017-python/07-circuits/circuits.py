# encoding: utf-8
""" Advent of Code 2017

`Day 7 <http://adventofcode.com/2017/day/7>`_:
Recursive Circuits
"""
from __future__ import division, print_function
import argparse
import collections
import itertools
import io


EXAMPLE = u"""
    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)
"""


class Forest(object):
    """ Build trees from a set of nodes. """

    def __init__(self):
        self.nodes = dict()
        self.parents = dict()

    def add_node(self, node, children):
        if str(node) in self.nodes:
            raise ValueError("duplicate node name {0}".format(str(node)))
        self.nodes[str(node)] = node
        for name in children:
            if name in self.parents:
                parents = [self.parents[name], node]
                raise ValueError("multiple parents for node {0}:"
                                 " {1}".format(name, parents))
            self.parents[name] = node

    def build(self):
        trees = []
        for node in self.nodes.itervalues():
            parent = self.parents.get(str(node), None)
            if parent:
                node.parent = parent
            else:
                node.parent = None
                trees.append(node)
        return trees


class TreeNode(object):
    """ A tree vertice. """

    def __init__(self, label, data):
        self.label = label
        self.data = data
        self._parent = None
        self._children = set()

    def __str__(self):
        return str(self.label)

    def __repr__(self):
        return '<TreeNode {0!r}>'.format(self.label)

    @property
    def path(self):
        """ a full list of nodees down to the bottom one. """
        return itertools.chain(
            (self, ),
            getattr(self.parent, 'path') if self.parent else ())

    @property
    def parent(self):
        """ the node that this node is pathed on top of. """
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        if new_parent is not None:
            if self in new_parent.path:
                raise ValueError(
                    "cycle in {!s}: {!s}".format(
                        self, " -> ".join(map(repr, new_parent.path))))

        # update old and new parent:
        if self._parent is not None:
            self._parent._children.remove(self)
        if new_parent is not None:
            new_parent._children.add(self)
        self._parent = new_parent

    @property
    def children(self):
        """ nodees on this node' children. """
        for node in self._children:
            yield node


def parse_node(nodestring):
    """ Parse a string with node information.

    :return tuple:
        Returns node data from the input string.  Each tuple consists of:
          - node name (str)
          - node weight (int)
          - node names on children (list<str>)
    """
    node, _, children = [p.strip() for p in nodestring.partition('->')]
    name, _, weight = [p.strip() for p in node.partition(' ')]
    weight = int(weight.strip('()'))
    if children:
        children = [c.strip() for c in children.split(',') if c.strip()]
    else:
        children = []
    return TreeNode(name, weight), children


def dump_tree(root, prefix=''):
    """ print a simple representation of the tree. """
    indents = [' │  ', '    ']
    markers = [" ├─ ", ' └─ ']

    def dump(root, prefix, is_last, is_root):
        marker = markers[int(is_last)] * int(not is_root)
        print("{0}{1}{2!r}".format(prefix, marker, root))
        children = list(root.children)
        for num, child in enumerate(children, 1):
            add_indent = '' if is_root else indents[bool(is_last)]
            dump(child, prefix + add_indent, num == len(children), False)
    dump(root, prefix, True, True)


def sum_tree(node):
    """ calculate the sum of data in this node and all its children. """
    return int(node.data) + sum(sum_tree(c) for c in node.children)


def find_imbalanced_node(node):
    """ Identify an imbalanced node.

    Finds a node that prevents the sum of that subtree from being balanced, and
    suggest a new value for that node.
    """
    child_sums = dict((str(c), sum_tree(c)) for c in node.children)
    sum_counts = collections.Counter(child_sums.values())
    if len(sum_counts) <= 1:
        # no children, or children are balanced.
        return None
    norm = sum_counts.most_common(1)[0][0]
    for c in node.children:
        difference = norm - child_sums[str(c)]
        if difference:
            # this child or one of its children breaks the norm
            return find_imbalanced_node(c) or (c, difference)
    raise RuntimeError("could not identify imbalanced node for some reason")


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'parent',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('Ur'),
        default=io.StringIO(EXAMPLE),
        help="file to read, or '-' to read from STDIN")
    parser.add_argument(
        '-d', '--dump-tree',
        dest='dump',
        action='store_true',
        default=False,
        help="Dump parent to STDOUT")
    skip = parser.add_mutually_exclusive_group()
    skip.add_argument(
        '--skip-part-1',
        dest='part_1',
        action='store_false',
        default=True,
        help="skip part 1")
    skip.add_argument(
        '--skip-part-2',
        dest='part_2',
        action='store_false',
        default=True,
        help="skip part 2")
    args = parser.parse_args(inargs)

    print('Reading nodees...')
    forest = Forest()
    with args.parent:
        for line in args.parent:
            if not line.strip():
                continue
            forest.add_node(*parse_node(line))
    print('...read {0} nodes'.format(len(forest.nodes)))

    roots = forest.build()
    if args.dump:
        for root in roots:
            dump_tree(root)

    if len(roots) < 1:
        raise ValueError('Input contains no nodes')
    if len(roots) > 1:
        raise ValueError('Input contains multiple root nodes')
    root = roots.pop()

    if args.part_1:
        print("Part 1: root node is {0}".format(root))

    if args.part_2:
        node, correction = find_imbalanced_node(root)
        weight = int(node.data) + correction
        print("Part 2: node {0!r} should weigh {1}".format(node, weight))


if __name__ == '__main__':
    main()
