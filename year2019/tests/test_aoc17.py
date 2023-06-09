from inspect import cleandoc

import pytest

from ..aoc17 import find_intersections, parse_tiles, solve, walk_through_all

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


@pytest.mark.parametrize(
    'sample, path',
    (
        (sample1, '4,R,2,R,2,R,12,R,2,R,6,R,4,R,4,R,6'),
        (sample2, 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'),
    ),
)
def test_walk_through_all(sample, path):
    tiles = parse_tiles(sample.split())
    assert ','.join(map(str, walk_through_all(tiles))) == path


def test_solve():
    assert solve() == (3292, 0)
