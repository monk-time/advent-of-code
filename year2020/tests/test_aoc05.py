from inspect import cleandoc

from year2020.aoc05 import parse, solve

sample = cleandoc("""
    FBFBBFFRLR
    BFFFBBFRRR
    FFFBBBFRRR
    BBFFBBFRLL
""")


def test_parse():
    assert list(parse(sample)) == [(44, 5), (70, 7), (14, 7), (102, 4)]


def test_solve():
    assert solve() == (963, 592)
