import pytest

from year2018.aoc09 import high_score, solve

samples = [
    ('9 players; last marble is worth 25 points', 32),
    ('10 players; last marble is worth 1618 points', 8317),
    ('13 players; last marble is worth 7999 points', 146373),
    ('17 players; last marble is worth 1104 points', 2764),
    ('21 players; last marble is worth 6111 points', 54718),
    ('30 players; last marble is worth 5807 points', 37305),
]


@pytest.mark.parametrize('input_str, result', samples)
def test_high_score(input_str, result):
    assert high_score(input_str) == result


def test_solve():
    assert solve() == (383475, 3148209772)
