from inspect import cleandoc
from typing import List

import pytest

from aoc23 import Nanobot, count_in_range, parse, solve

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
def sample() -> List[Nanobot]:
    return parse(sample_str)


def test_parse(sample):
    assert sample == [
        Nanobot((0, 0, 0), r=4),
        Nanobot((1, 0, 0), r=1),
        Nanobot((4, 0, 0), r=3),
        Nanobot((0, 2, 0), r=1),
        Nanobot((0, 5, 0), r=3),
        Nanobot((0, 0, 3), r=1),
        Nanobot((1, 1, 1), r=1),
        Nanobot((1, 1, 2), r=1),
        Nanobot((1, 3, 1), r=1),
    ]


def test_is_in_range(sample):
    bot = sample[0]
    assert list(map(bot.is_in_range, sample)) == \
           [True, True, True, True, False, True, True, True, False]


def test_count_in_range(sample):
    assert count_in_range(sample) == 7


def test_solve():
    assert solve() == 172
