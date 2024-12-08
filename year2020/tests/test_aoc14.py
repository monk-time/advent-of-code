from inspect import cleandoc

from year2020.aoc14 import parse, run, run_v2, solve

sample1 = cleandoc("""
    mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    mem[8] = 11
    mem[7] = 101
    mem[8] = 0
""")

sample2 = cleandoc("""
    mask = 000000000000000000000000000000X1001X
    mem[42] = 100
    mask = 00000000000000000000000000000000X0XX
    mem[26] = 1
""")


def test_run():
    assert run(parse(sample1)) == 165


def test_run_v2():
    assert run_v2(parse(sample2)) == 208


def test_solve():
    assert solve() == (15018100062885, 5724245857696)
