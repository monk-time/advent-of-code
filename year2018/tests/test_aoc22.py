from inspect import cleandoc

import pytest

from aoc22 import Map, calc_risk, solve

sample_str = cleandoc("""
    depth: 510
    target: 10,10
""")


@pytest.fixture
def sample():
    return Map(sample_str)


def test_map_init(sample):
    assert sample.depth == 510
    assert sample.target == (10, 10)
    assert len(sample.erosion.keys()) == 121
    assert sample.erosion[(0, 0)] == 510
    assert sample.erosion[(0, 1)] == 17317
    assert sample.erosion[(1, 0)] == 8415
    assert sample.erosion[(1, 1)] == 1805
    assert sample.erosion[(10, 10)] == 510
    assert sample.cave[(0, 0)] == 'M'
    assert sample.cave[(0, 1)] == '='
    assert sample.cave[(1, 0)] == '.'
    assert sample.cave[(1, 1)] == '|'
    assert sample.cave[(10, 10)] == 'T'


def test_map_str(sample):
    assert str(sample) == cleandoc("""
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


def test_map_gen_deeper(sample):
    sample.gen_deeper()
    assert str(sample) == cleandoc("""
        M=.|=.|.|=.|
        .|=|=|||..|.
        .==|....||=.
        =.|....|.==.
        =|..==...=.|
        =||.=.=||=|=
        |.=.===|||..
        |..==||=.|==
        .=..===..=|.
        .======|||=|
        .===|=|===T=
        =|||...|==..
    """)

    sample.gen_deeper()
    assert str(sample) == cleandoc("""
        M=.|=.|.|=.|=
        .|=|=|||..|.=
        .==|....||=..
        =.|....|.==.|
        =|..==...=.|=
        =||.=.=||=|=.
        |.=.===|||..=
        |..==||=.|==|
        .=..===..=|.|
        .======|||=|=
        .===|=|===T==
        =|||...|==..|
        =.=|=.=..=.||
    """)


def test_solve():
    assert solve() == 10115
