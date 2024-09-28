from inspect import cleandoc

from year2020.aoc12 import parse, part1, part2, solve

sample = cleandoc("""
    F10
    N3
    F7
    R90
    F11
""")


def test_part1():
    assert part1(parse(sample)) == 25


def test_part2():
    assert part2(parse(sample)) == 286


def test_solve():
    assert solve() == (1710, 62045)
