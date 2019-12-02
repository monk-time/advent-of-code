from inspect import cleandoc

import pytest

from aoc22 import calc_risk, gen_map, map_to_str, parse, solve

sample_str = cleandoc("""
    depth: 510
    target: 10,10
""")


@pytest.fixture
def sample():
    return gen_map(*parse(sample_str))


def test_parse():
    assert parse(sample_str) == (510, (10, 10))


def test_gen_map(sample):
    assert len(sample) == 121
    assert sample[(0, 0)] == 510
    assert sample[(0, 1)] == 17317
    assert sample[(1, 0)] == 8415
    assert sample[(1, 1)] == 1805
    assert sample[(10, 10)] == 510


def test_map_to_str(sample):
    assert map_to_str(sample) == cleandoc("""
        M=.|=.|.|=.
        .|=|=|||..|
        .==|....||=
        =.|....|.==
        =|..==...=.
        =||.=.=||=|
        |.=.===|||.
        |..==||=.|=
        .=..===..=|
        .======|||=
        .===|=|===T
    """)


def test_calc_risk(sample):
    assert calc_risk(sample) == 114


def test_solve():
    assert solve() == 10115
