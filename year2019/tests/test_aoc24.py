from inspect import cleandoc

import pytest

from year2019.aoc24 import parse, part1, part2, solve, update_grid

sample1 = cleandoc("""
    ....#
    #..#.
    #..##
    ..#..
    #....
""")

sample2 = cleandoc("""
    #..#.
    ####.
    ###.#
    ##.##
    .##..
""")

sample3 = cleandoc("""
    #####
    ....#
    ....#
    ...#.
    #.###
""")

sample4 = cleandoc("""
    #....
    ####.
    ...##
    #.##.
    .##.#
""")

sample5 = cleandoc("""
    ####.
    ....#
    ##..#
    .....
    ##...
""")

sample_bio = cleandoc("""
    .....
    .....
    .....
    #....
    .#...
""")


@pytest.mark.parametrize(
    'sample, result',
    (
        (sample1, sample2),
        (sample2, sample3),
        (sample3, sample4),
        (sample4, sample5),
    ),
)
def test_update_grid(sample: str, result: str):
    assert update_grid(parse(sample)) == parse(result)


def test_part1():
    assert part1(parse(sample1)) == 2129920


def test_part2():
    assert part2(parse(sample1), 10) == 99


def test_solve():
    assert solve() == (17863741, 2029)
