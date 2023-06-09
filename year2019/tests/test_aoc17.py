from inspect import cleandoc
from ..aoc17 import find_intersections, parse_tiles, solve

sample1 = cleandoc(
    """
    ..#..........
    ..#..........
    #######...###
    #.#...#...#.#
    #############
    ..#...#...#..
    ..#####...^..
    """
)

sample2 = cleandoc(
    """
    #######...#####
    #.....#...#...#
    #.....#...#...#
    ......#...#...#
    ......#...###.#
    ......#.....#.#
    ^########...#.#
    ......#.#...#.#
    ......#########
    ........#...#..
    ....#########..
    ....#...#......
    ....#...#......
    ....#...#......
    ....#####......
    """
)


def test_find_intersections():
    tiles = parse_tiles(sample1.split())
    assert list(find_intersections(tiles)) == [(2, 2), (2, 4), (6, 4), (10, 4)]


def test_solve():
    assert solve() == (3292, 0)
