import pytest

from year2020.aoc23 import (
    Links,
    pad,
    parse,
    part1,
    part2,
    simulate,
    solve,
    to_str,
)

sample = '389125467'


@pytest.fixture
def links() -> Links:
    return parse(sample)


def test_to_str(links: Links):
    assert to_str(links) == '3 8 9 1 2 5 4 6 7'
    assert to_str(links, start=1) == '1 2 5 4 6 7 3 8 9'


def test_simulate(links: Links):
    assert to_str(simulate(links, 10)) == '8 3 7 4 1 9 2 6 5'


def test_part1(links: Links):
    assert part1(links) == '67384529'


def test_pad(links: Links):
    assert to_str(pad(links, 12)) == '3 8 9 1 2 5 4 6 7 10 11 12'


def test_part2(links: Links):
    assert part2(links) == 149245887792


def test_solve():
    assert solve() == ('38756249', 21986479838)
