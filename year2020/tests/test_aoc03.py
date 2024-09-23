from inspect import cleandoc

import pytest

from year2020.aoc03 import count_trees, parse, solve

sample = cleandoc("""
    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#
""")


@pytest.mark.parametrize(
    'slope, result',
    (((1, 1), 2), ((3, 1), 7), ((5, 1), 3), ((7, 1), 4), ((1, 2), 2)),
)
def test_count_trees(slope, result):
    assert count_trees(parse(sample), *slope) == result


def test_solve():
    assert solve() == (171, 1206576000)
