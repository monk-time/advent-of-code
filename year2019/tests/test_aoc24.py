from inspect import cleandoc

import pytest

from year2019.aoc24 import calc_bio, parse, part1, solve, update_grid

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
def test_update_grid(sample, result):
    assert update_grid(parse(sample)) == parse(result)


def test_calc_bio():
    assert calc_bio(parse(sample_bio)) == 2129920


def test_part1():
    assert part1(parse(sample1)) == 2129920


def test_solve():
    assert solve() == (0, 0)
