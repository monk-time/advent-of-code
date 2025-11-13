from inspect import cleandoc

import pytest

from year2018.aoc23 import (
    Bot,
    count_in_range,
    is_in_range,
    parse,
    shortest_manhattan,
    solve,
)

sample_str = cleandoc("""
    pos=<0,0,0>, r=4
    pos=<1,0,0>, r=1
    pos=<4,0,0>, r=3
    pos=<0,2,0>, r=1
    pos=<0,5,0>, r=3
    pos=<0,0,3>, r=1
    pos=<1,1,1>, r=1
    pos=<1,1,2>, r=1
    pos=<1,3,1>, r=1
""")


@pytest.fixture
def sample() -> list[Bot]:
    return parse(sample_str)


def test_parse(sample: str):
    assert sample == [
        Bot((0, 0, 0), 4),
        Bot((1, 0, 0), 1),
        Bot((4, 0, 0), 3),
        Bot((0, 2, 0), 1),
        Bot((0, 5, 0), 3),
        Bot((0, 0, 3), 1),
        Bot((1, 1, 1), 1),
        Bot((1, 1, 2), 1),
        Bot((1, 3, 1), 1),
    ]


def test_is_in_range(sample: list[Bot]):
    bot = sample[0]
    assert [is_in_range(bot, b) for b in sample] == [
        True,
        True,
        True,
        True,
        False,
        True,
        True,
        True,
        False,
    ]


def test_count_in_range(sample: list[Bot]):
    assert count_in_range(sample) == 7


def test_shortest_manhattan():
    bots = parse(
        cleandoc("""
            pos=<10,12,12>, r=2
            pos=<12,14,12>, r=2
            pos=<16,12,12>, r=4
            pos=<14,14,14>, r=6
            pos=<50,50,50>, r=200
            pos=<10,10,10>, r=5
        """)
    )
    assert shortest_manhattan(bots) == 36


def test_solve():
    assert solve() == (172, 125532607)
