from inspect import cleandoc

import pytest

from aoc25 import count_constellations, dist, parse, solve


def test_parse():
    assert parse(cleandoc("""
        -1,2,2,0
        0,0,2,-2
    """)) == [(-1, 2, 2, 0), (0, 0, 2, -2)]


def test_dist():
    assert dist((0, 0, 0, 0), (3, 0, 0, 0)) == 3
    assert dist((1, 0, -1, 0), (3, 0, 4, 0)) == 7


@pytest.mark.parametrize('s, n', (
        (cleandoc("""
             0,0,0,0
             3,0,0,0
             0,3,0,0
             0,0,3,0
             0,0,0,3
             0,0,0,6
             9,0,0,0
            12,0,0,0
        """), 2),
        (cleandoc("""
            -1,2,2,0
            0,0,2,-2
            0,0,0,-2
            -1,2,0,0
            -2,-2,-2,2
            3,0,2,-1
            -1,3,2,2
            -1,0,-1,0
            0,2,1,-2
            3,0,0,0
        """), 4),
        (cleandoc("""
            1,-1,0,1
            2,0,-1,0
            3,2,-1,0
            0,0,3,1
            0,0,-1,-1
            2,3,-2,0
            -2,2,0,0
            2,-2,0,-1
            1,-1,0,-1
            3,2,0,2
        """), 3),
        (cleandoc("""
            1,-1,-1,-2
            -2,-2,0,1
            0,2,1,3
            -2,3,-2,1
            0,2,3,-2
            -1,-1,1,-2
            0,-2,-1,0
            -2,2,3,-1
            1,2,2,0
            -1,-2,0,-2
        """), 8),
))
def test_count_constellations(s, n):
    assert count_constellations(parse(s)) == n


def test_solve():
    assert solve() == 399
