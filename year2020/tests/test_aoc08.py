from inspect import cleandoc

from year2020.aoc08 import Result, fix, parse, run, solve

sample = cleandoc("""
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
""")


def test_run():
    assert run(parse(sample)) == Result(acc=5, inf_loop=True)


def test_fix():
    assert fix(parse(sample)) == Result(acc=8, inf_loop=False)


def test_solve():
    assert solve() == (1832, 662)
