import pytest

from year2020.aoc23 import pad, parse, part1, part2, simulate, solve

sample = '389125467'


@pytest.fixture
def node():
    return parse(sample)


def test_pad(node):
    assert pad(node, 12).to_str() == '3 8 9 1 2 5 4 6 7 10 11 12'


def test_simulate(node):
    assert simulate(node, 10).to_str() == '1 9 2 6 5 8 3 7 4'


def test_part1(node):
    assert part1(node) == '67384529'


def test_part2(node):
    assert part2(node) == 149245887792


def test_solve():
    assert solve() == ('38756249', 21986479838)
