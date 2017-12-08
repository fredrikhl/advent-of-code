""" Advent of Code 2017

`Day 8 <http://adventofcode.com/2017/day/6>`_:
I Heard You Like Registers
"""
from __future__ import print_function
import argparse
import functools
import operator
import io


EXAMPLE = u"""
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""


class Operators(dict):
    """ A dictionary that maps operator names to functions. """

    def register(self, *opnames):
        """ Get a function decorator to register callback.

        The decorator will simply add the function under the keys in `opnames`.

        Example:

        >>> ops = Operators()
        >>> @ops.register('foo', 'bar')
        ... def foo():
        ...     pass
        >>> assert ops['foo'] == ops['bar'] == foo
        """
        def wrapper(func):
            for opname in opnames:
                self[opname] = func
            return func
        return wrapper

    def __setitem__(self, opname, opfunc):
        if opname in self:
            raise KeyError("operator {0} already set".format(opname))
        super(Operators, self).__setitem__(opname, opfunc)

    def __call__(self, operator, *args, **kwargs):
        return self[operator](*args, **kwargs)

    def __repr__(self):
        return '<Operators {0}>'.format(','.join(self.keys()))


class Expression(object):
    """ A basic expression.

    Example:

    >>> expression = Expression.parse('foo inc 10')
    >>> assert expression.function(7, 2) == 9
    >>> assert expression.name == 'foo'
    >>> assert expression.value == 10
    >>> namespace = dict(foo=5)
    >>> expression(namespace)
    >>> assert namespace['foo'] == 15

    """

    operators = Operators({
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        'inc': operator.add,
        'dec': operator.sub,
    })

    @classmethod
    def parse(cls, expression):
        """ Parse an infix expression.

        :param str expression:
            An infix expression, with format:
            "<identifier> <operator> <literal>"

        :return Expression:
            Returns the parsed expression.
        """
        identifier, operator, literal = expression.split()
        assert identifier
        assert operator in cls.operators
        literal = int(literal)
        return cls(identifier, operator, literal)

    @property
    def function(self):
        """ operator function. """
        return functools.partial(self.operators, self.opname)

    def __init__(self, identifier, operator, literal):
        self.name = identifier
        assert operator in self.operators
        self.opname = operator
        self.value = literal

    def __repr__(self):
        return '<Expression[{0.name} {0.opname} {0.value}]>'.format(self)

    def __call__(self, namespace):
        """ Run the expression with a namespace of identifiers.

        :param dict namespace:
            A dict-like object with identifiers as keys.

        :return:
            Returns the result of the expression.
        """
        return self.function(namespace[self.name], self.value)


class Namespace(dict):
    """ A namespace dict for identifiers and numbers.

    All identifiers are numbers, and missing missing identifiers are set to 0.
    The namespace tracks the highest identifier value in its lifetime.
    """

    def __init__(self):
        self.all_time_high = None
        super(Namespace, self).__init__()

    def __missing__(self, key):
        self[key] = 0
        return self[key]

    def __setitem__(self, key, value):
        super(Namespace, self).__setitem__(key, value)
        if self.all_time_high is None:
            self.all_time_high = (key, value)
        else:
            self.all_time_high = max((key, value), self.all_time_high,
                                     key=operator.itemgetter(1))

    def __repr__(self):
        return '<{0} size={1}>'.format(self.__class__.__name__, len(self))

    @property
    def high(self):
        """ the current highest identifier value. """
        if len(self) == 0:
            return None
        return max(self.items(), key=operator.itemgetter(1))


def parse_statement(statement):
    """ parse an if-statement.

    :param str statement:
        An if-statement with syntax: "<expression> if <expression>"

    :return tuple:
        Returns a tuple with two Expression objects, the latter being the
        condition.
    """
    expression, _, condition = statement.strip().partition('if')
    return (Expression.parse(expression), Expression.parse(condition))


def run(namespace, expression, condition):
    if condition(namespace):
        namespace[expression.name] = expression(namespace)


def main(inargs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'program',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('Ur'),
        default=io.StringIO(EXAMPLE),
        help="file with program to read, or '-' to read from STDIN")
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

    print('Reading program...')
    with args.program:
        statements = [parse_statement(line)
                      for line in args.program if line.strip()]
    print('{0} statements read'.format(len(statements)))

    if not statements:
        raise RuntimeError("no statements to execute")

    namespace = Namespace()

    for expr, cond in statements:
        run(namespace, expr, cond)

    if args.part_1:
        print("Part 1: {0[0]} = {0[1]}".format(namespace.high))

    if args.part_2:
        print("Part 2: {0[0]} = {0[1]}".format(namespace.all_time_high))


if __name__ == '__main__':
    main()
