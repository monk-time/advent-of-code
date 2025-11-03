from inspect import cleandoc

from year2020.aoc22 import combat, parse, recursive_combat, score, solve

sample = cleandoc("""
    Player 1:
    9
    2
    6
    3
    1

    Player 2:
    5
    8
    4
    7
    10
""")

sample_inf = cleandoc("""
    Player 1:
    43
    19

    Player 2:
    2
    29
    14
""")


def test_combat():
    p1, p2 = parse(sample)
    assert score(combat(p1, p2)) == 306


def test_recursive_combat():
    p1, p2 = parse(sample)
    assert score(recursive_combat(p1, p2)) == 291


def test_inf_loop():
    p1, p2 = parse(sample_inf)
    assert score(recursive_combat(p1, p2)) == 105


def test_solve():
    assert solve() == (32413, 31596)
