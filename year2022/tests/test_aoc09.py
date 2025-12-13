from inspect import cleandoc

from year2022.aoc09 import parse, part1, solve

sample = cleandoc("""
""")


def test_part1():
    assert part1(parse(sample)) == 0


def test_solve():
    assert solve() == (0, 0)
