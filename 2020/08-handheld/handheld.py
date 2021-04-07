"""
AoC Day 8: Handheld Halting
"""
import os
import sys


# State tuple indices
IP, ACC = 0, 1


def op_nop(state, arg):
    return (state[IP] + 1, state[ACC])


def op_acc(state, arg):
    return (state[IP] + 1, state[ACC] + arg)


def op_jmp(state, arg):
    return (state[IP] + arg, state[ACC])


OPERATORS = {'nop': op_nop, 'acc': op_acc, 'jmp': op_jmp}


def parse_line(text):
    """ parse line into (operator, argument) tuple. """
    op, sep, arg = text.partition(' ')
    if not sep:
        raise ValueError('invalid instruction')
    if op not in OPERATORS:
        raise ValueError('invalid operator %r' % op)
    return OPERATORS[op], int(arg)


def parse_file(fd):
    """ read instructins from a file-like object. """
    for lineno, line in enumerate(fd, 1):
        try:
            yield parse_line(line.rstrip())
        except Exception as e:
            raise ValueError('error on line %d (%r): %s' % (lineno, line, e))


def step(program, state):
    """ execute next program instruction. """
    ip = state[IP]
    if 0 <= ip < len(program):
        op, arg = program[ip]
        return op(state, arg)
    raise RuntimeError("Instruction %d is out of bounds (0, %d)" %
                       (ip, len(program)))


def run(program, state):
    """ run program until termination. """
    while True:
        try:
            yield (state := step(program, state))  # noqa: E203, E231
        except RuntimeError:
            # out of bounds - done
            break


def find_loop(program):
    """ find loop in program. """
    state = (0, 0)
    seen = set((state[IP],))
    for state in run(program, state):
        if state[IP] in seen:
            return True, state
        seen.add(state[IP])
    return False, state


def replace_op(program, ip, op):
    """ replace operator at a given instruction. """
    old_op, arg = program[ip]
    return program[:ip] + ((op, arg),) + program[ip+1:]


def fix_loop(program):
    """ swap nop/jmp until loop is fixed. """
    for i, (op, _) in enumerate(program):
        if op is op_jmp:
            op = op_nop
        elif op is op_nop:
            op = op_jmp
        else:
            continue

        loop, state = find_loop(replace_op(program, i, op))
        if not loop:
            return i, state

    return -1, state


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main(inargs=None):
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        program = tuple(parse_file(f))

    found, state = find_loop(program)
    if not found:
        raise RuntimeError('unable to find loop (state=%s)' % repr(state))
    print("Part 1: %d" % state[ACC])

    i, state = fix_loop(program)
    if i < 0:
        raise RuntimeError('Part 2: unable to fix loop (state=%s)' %
                           repr(state))
    print("Part 2: %d" % state[ACC])


if __name__ == '__main__':
    main()
