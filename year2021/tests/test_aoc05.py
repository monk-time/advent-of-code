from inspect import cleandoc

import pytest

from year2021.aoc05 import Coord, count_overlaps, line, parse, solve

sample = cleandoc("""
    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2
""")


@pytest.mark.parametrize(
    'a, b, with_diag, result',
    (
        ((1, 5), (3, 5), False, [(1, 5), (2, 5), (3, 5)]),
        ((3, 5), (1, 5), False, [(3, 5), (2, 5), (1, 5)]),
        ((5, 1), (5, 3), False, [(5, 1), (5, 2), (5, 3)]),
        ((5, 3), (5, 1), False, [(5, 3), (5, 2), (5, 1)]),
        ((1, 5), (3, 7), True, [(1, 5), (2, 6), (3, 7)]),
        ((3, 7), (1, 5), True, [(3, 7), (2, 6), (1, 5)]),
        ((1, 7), (3, 5), True, [(1, 7), (2, 6), (3, 5)]),
        ((3, 5), (1, 7), True, [(3, 5), (2, 6), (1, 7)]),
    ),
)
def test_line(a: Coord, b: Coord, with_diag: bool, result: list[Coord]):  # noqa: FBT001
    assert list(line(a, b, with_diag=with_diag)) == result


def test_count_overlaps():
    assert count_overlaps(parse(sample)) == 5


def test_count_overlaps_with_diag():
    assert count_overlaps(parse(sample), with_diag=True) == 12


def test_solve():
    assert solve() == (6189, 19164)
