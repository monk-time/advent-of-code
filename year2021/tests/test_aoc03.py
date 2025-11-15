from inspect import cleandoc

import pytest

from year2021.aoc03 import (
    Report,
    calc_life_support,
    calc_power,
    parse,
    solve,
)

sample = cleandoc("""
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010
""")


@pytest.fixture(scope='module')
def report() -> Report:
    return parse(sample)


def test_calc_power(report: Report):
    assert calc_power(report) == 198


def test_calc_life_support(report: Report):
    assert calc_life_support(report) == 230


def test_solve():
    assert solve() == (1025636, 793873)
