from inspect import cleandoc

import pytest

from aoc16 import execute, matches, opcodes, parse, solve


def test_parse():
    s = cleandoc("""
        Before: [1, 0, 2, 0]
        4 1 0 1
        After:  [1, 1, 2, 0]
        
        Before: [2, 3, 1, 2]
        2 1 0 1
        After:  [2, 1, 1, 2]
        
        
        
        9 3 3 0
        9 1 0 1
        """)
    assert parse(s) == (
        [
            ((1, 0, 2, 0), (4, 1, 0, 1), (1, 1, 2, 0)),
            ((2, 3, 1, 2), (2, 1, 0, 1), (2, 1, 1, 2))
        ],
        [(9, 3, 3, 0), (9, 1, 0, 1)]
    )


samples = (
    ((('addr', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 6)),
    ((('addi', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 5)),
    ((('mulr', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 8)),
    ((('muli', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 4)),
    ((('banr', 0, 1, 3), (3, 2, 1, 3)), (3, 2, 1, 2)),
    ((('bani', 0, 1, 3), (3, 2, 1, 3)), (3, 2, 1, 1)),
    ((('borr', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 6)),
    ((('bori', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 5)),
    ((('setr', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 4)),
    ((('seti', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 0)),
    ((('gtir', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 0)),
    ((('gtri', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 1)),
    ((('gtrr', 0, 1, 3), (4, 2, 1, 3)), (4, 2, 1, 1)),
    ((('eqir', 0, 1, 3), (4, 4, 1, 3)), (4, 4, 1, 0)),
    ((('eqri', 0, 1, 3), (4, 4, 1, 3)), (4, 4, 1, 0)),
    ((('eqrr', 0, 1, 3), (4, 4, 1, 3)), (4, 4, 1, 1)),
)


@pytest.mark.parametrize("args, reg_after", samples)
def test_execute(args, reg_after):
    instr, reg = args
    instr = (opcodes.index(instr[0]), *instr[1:])
    assert execute(instr, reg) == reg_after


def test_execute_immutable():
    reg = (1, 2, 3, 4)
    reg_copy = tuple(reg)
    execute((0, 0, 1, 3), reg)
    assert reg == reg_copy


def test_matches():
    assert matches((3, 2, 1, 1), (9, 2, 1, 2), (3, 2, 2, 1)) == [1, 2, 9]


def test_solve():
    assert solve() == (509, 496)
