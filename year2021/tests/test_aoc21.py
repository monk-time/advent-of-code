from inspect import cleandoc

from year2021.aoc21 import parse, play_deterministic, play_dirac, solve

sample = cleandoc("""
    Player 1 starting position: 4
    Player 2 starting position: 8
""")


def test_play_deterministic():
    assert play_deterministic(parse(sample)) == 739785


def test_play_dirac():
    assert play_dirac(parse(sample)) == 444356092776315


def test_solve():
    assert solve() == (920580, 647920021341197)
