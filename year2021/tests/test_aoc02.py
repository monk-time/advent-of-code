from inspect import cleandoc

from year2021.aoc02 import parse, solve, travel

sample = cleandoc("""
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
""")


def test_travel():
    assert travel(parse(sample)) == 150


def test_travel_with_aim():
    assert travel(parse(sample), with_aim=True) == 900


def test_solve():
    assert solve() == (2073315, 1840311528)
