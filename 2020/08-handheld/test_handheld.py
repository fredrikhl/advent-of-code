import io

import handheld as mod


example_text = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""".strip()


example = (
    (mod.op_nop, 0),
    (mod.op_acc, 1),
    (mod.op_jmp, 4),
    (mod.op_acc, 3),
    (mod.op_jmp, -3),
    (mod.op_acc, -99),
    (mod.op_acc, 1),
    (mod.op_jmp, -4),
    (mod.op_acc, 6),
)


def test_parse_line():
    assert mod.parse_line('nop -1') == (mod.op_nop, -1)
    assert mod.parse_line('acc +4') == (mod.op_acc, 4)
    assert mod.parse_line('jmp -0') == (mod.op_jmp, 0)


def test_nop():
    assert mod.op_nop((0, 0), 0) == (1, 0)


def test_acc():
    assert mod.op_acc((0, 0), 3) == (1, 3)
    assert mod.op_acc((0, 0), -3) == (1, -3)


def test_jmp():
    assert mod.op_jmp((0, 0), 3) == (3, 0)
    assert mod.op_jmp((0, 0), -3) == (-3, 0)


def test_parse_file():
    with io.StringIO(example_text) as f:
        assert tuple(mod.parse_file(f)) == example


def test_step():
    assert mod.step(example, (0, 0)) == (1, 0)
    assert mod.step(example, (1, 0)) == (2, 1)
    assert mod.step(example, (2, 1)) == (6, 1)


def test_step_oob():
    try:
        mod.step(example, (len(example), 0))
    except RuntimeError:
        assert True
    else:
        assert False


def test_replace_op():
    result = example
    result = mod.replace_op(result, 0, mod.op_jmp)
    result = mod.replace_op(result, 4, mod.op_nop)
    assert example[0] == (mod.op_nop, 0)
    assert result[0] == (mod.op_jmp, 0)
    assert example[4] == (mod.op_jmp, -3)
    assert result[4] == (mod.op_nop, -3)


def test_find_loop():
    found, state = mod.find_loop(example)
    assert found
    assert state == (1, 5)


def test_fix_loop():
    i, state = mod.fix_loop(example)
    assert i == 7
    assert state == (9, 8)
