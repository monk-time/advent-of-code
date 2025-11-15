from inspect import cleandoc

import pytest

from year2021.aoc01 import (
    count_increases,
    parse,
    solve,
)

sample = cleandoc("""
    199
    200
    208
    210
    200
    207
    240
    269
    260
    263
""")


@pytest.mark.parametrize('window, result', ((1, 7), (3, 5)))
def test_count_increases(window: int, result: int):
    assert count_increases(parse(sample), window=window) == result


def test_solve():
    assert solve() == (1655, 1683)
