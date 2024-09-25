import pytest

from year2020.aoc10 import count_chains, difference, solve

sample1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
sample2 = [
    28,
    33,
    18,
    42,
    31,
    14,
    46,
    20,
    48,
    47,
    24,
    23,
    49,
    45,
    19,
    38,
    39,
    11,
    1,
    32,
    25,
    35,
    8,
    17,
    7,
    9,
    4,
    2,
    34,
    10,
    3,
]


@pytest.mark.parametrize('arr, result', ((sample1, 35), (sample2, 220)))
def test_difference(arr, result):
    assert difference(arr) == result


@pytest.mark.parametrize('arr, result', ((sample1, 8), (sample2, 19208)))
def test_count_chains(arr, result):
    assert count_chains(arr) == result


def test_solve():
    assert solve() == (2368, 1727094849536)
