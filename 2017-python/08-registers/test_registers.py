""" Advent of Code 2017, Day 8 tests """
from registers import Operators, Expression, Namespace, run


def example_op(a, b):
    return a ** b


def test_operators_set():
    ops = Operators()
    ops['foo'] = example_op
    assert len(ops) == 1
    assert 'foo' in ops
    assert ops['foo'] is example_op


def test_operators_call():
    ops = Operators()
    ops['foo'] = example_op
    assert ops('foo', 2, 2) == 4


def test_operators_register():
    ops = Operators()

    @ops.register('foo', 'bar')
    def test():
        pass

    assert all(k in ops for k in ('foo', 'bar'))
    assert ops['foo'] is ops['bar']
    assert ops['foo'] is test


def test_operators_init():
    ops = Operators(foo=example_op)
    assert len(ops) == 1
    assert 'foo' in ops
    assert ops['foo'] is example_op


def test_expression_operators():
    opnames = ('>', '<', '>=', '<=', '==', '!=', 'inc', 'dec',)
    assert all(
        opname in Expression.operators
        for opname in opnames)


def test_expression_parse():
    e = Expression.parse('b inc 5')
    assert e.opname == 'inc'
    assert e.name == 'b'
    assert e.value == 5

    e = Expression.parse('b == -20')
    assert e.opname == '=='
    assert e.name == 'b'
    assert e.value == -20


def test_expression_call():
    e = Expression('b', 'dec', -20)
    assert e(dict(b=0)) == 20

    e = Expression('b', '==', 0)
    assert e(dict(b=0)) is True


def test_empty_register_high():
    reg = Namespace()
    assert reg.high is None


def test_register_missing():
    reg = Namespace()

    assert 'a' not in reg
    assert reg['a'] == 0
    assert 'a' in reg


def test_register_high():
    reg = Namespace()
    reg['a'] = reg['b'] + 10
    assert reg.high == ('a', 10)


def test_register_high_default():
    reg = Namespace()
    reg['a'] = reg['c'] - 10
    reg['b'] = -5
    assert reg.high == ('c', 0)


def test_register_high_reset():
    reg = Namespace()
    reg['a'] = reg['b'] + 10
    assert reg.high == ('a', 10)
    reg['a'] = -5
    assert reg.high == ('b', 0)


def test_all_time_high_register():
    r = Namespace()

    assert r.all_time_high is None

    r['a'] = 10
    assert r['a'] == 10
    assert r['b'] == 0

    assert r.high == ('a', 10)
    assert r.all_time_high == ('a', 10)

    r['a'] = -5
    assert r.high == ('b', 0)
    assert r.all_time_high == ('a', 10)


def test_run_cond_true():
    reg = dict(a=10, b=0)
    inst = Expression('a', 'inc', 1)
    cond_true = Expression('b', '==', 0)

    run(reg, inst, cond_true)
    assert reg['a'] == 11


def test_run_cond_false():
    reg = dict(a=10, b=0)
    inst = Expression('a', 'inc', 1)
    cond_false = Expression('b', '!=', 0)

    run(reg, inst, cond_false)
    assert reg['a'] == 10


def example():
    return (
        (Expression('b', 'inc', 5),   Expression('a', '>', 1)),
        (Expression('a', 'inc', 1),   Expression('b', '<', 5)),
        (Expression('c', 'dec', -10), Expression('a', '>=', 1)),
        (Expression('c', 'inc', -20), Expression('c', '==', 10))
    )


def test_example_part_1():
    register = Namespace()
    for instruction, condition in example():
        run(register, instruction, condition)
        print(register)

    assert register.high[1] == 1


def test_example_part_2():
    register = Namespace()
    for instruction, condition in example():
        run(register, instruction, condition)
        print(register)

    assert register.high[1] == 1
    assert register.all_time_high[1] == 10
