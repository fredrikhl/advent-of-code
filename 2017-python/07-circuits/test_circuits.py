""" Advent of Code 2017, Day 7 tests """
from circuits import TreeNode, parse_node, Forest, sum_tree


def test_treenode_create():
    node = TreeNode('label', 'data')
    assert node.label == 'label'
    assert node.data == 'data'
    assert node.parent is None
    assert list(node.path) == [node, ]


def test_treenode_path():
    a = TreeNode('a', None)
    b = TreeNode('b', None)

    b.parent = a

    assert list(a.path) == [a, ]
    assert list(b.path) == [b, a]


def test_treenode_children():
    root_a = TreeNode('a', None)
    root_b = TreeNode('b', None)
    c = TreeNode('c', None)

    assert list(root_a.children) == []
    assert list(root_b.children) == []

    c.parent = root_a
    assert list(root_a.children) == [c, ]
    assert list(root_b.children) == []

    c.parent = root_b
    assert list(root_a.children) == []
    assert list(root_b.children) == [c, ]


def test_parse_node():
    node, children = parse_node("foo (10)")
    assert node.label == 'foo'
    assert node.data == 10
    assert list(children) == []

    node, children = parse_node("foo (10) -> bar")
    assert node.label == 'foo'
    assert node.data == 10
    assert list(children) == ['bar', ]

    node, children = parse_node("foo (10) -> bar, baz")
    assert node.label == 'foo'
    assert node.data == 10
    assert list(children) == ['bar', 'baz']


def test_forest_roots():
    a, b, c = (TreeNode(label, None) for label in ('a', 'b', 'c'))
    forest = Forest()

    forest.add_node(a, ())
    forest.add_node(b, ['c'])
    forest.add_node(c, ())

    roots = forest.build()
    assert len(roots) == 2
    assert a in roots
    assert b in roots
    assert c not in roots
    assert c.parent is b


def test_sum_tree():
    a, b, c = (TreeNode(label, 10) for label in ('a', 'b', 'c'))

    c.parent = a
    assert sum_tree(c) == 10
    assert sum_tree(a) == 20

    b.parent = a
    assert sum_tree(c) == 10
    assert sum_tree(b) == 10
    assert sum_tree(a) == 30
