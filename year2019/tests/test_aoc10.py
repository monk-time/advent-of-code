from inspect import cleandoc

import pytest

from year2019.aoc10 import (
    count_visible_from,
    find_best_location,
    parse,
    solve,
    vaporize_from,
)

m1 = parse(
    cleandoc(
        """
        .#..#
        .....
        #####
        ....#
        ...##
        """
    )
)

m2 = parse(
    cleandoc(
        """
        ......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####
        """
    )
)

m3 = parse(
    cleandoc(
        """
        #.#...#.#.
        .###....#.
        .#....#...
        ##.#.#.#.#
        ....#.#.#.
        .##..###.#
        ..#...##..
        ..##....##
        ......#...
        .####.###.
        """
    )
)

m4 = parse(
    cleandoc(
        """
        .#..#..###
        ####.###.#
        ....###.#.
        ..###.##.#
        ##.##.#.#.
        ....###..#
        ..#.#..#.#
        #..#.#.###
        .##...##.#
        .....#.#..
        """
    )
)

m5 = parse(
    cleandoc(
        """
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
        """
    )
)


@pytest.mark.parametrize(
    'x, y, expected',
    (
        (1, 0, 7),
        (4, 0, 7),
        (0, 2, 6),
        (1, 2, 7),
        (2, 2, 7),
        (3, 2, 7),
        (4, 2, 5),
        (4, 3, 7),
        (3, 4, 8),
        (4, 4, 7),
    ),
)
def test_count_visible_from(x, y, expected):
    assert count_visible_from(x, y, m1) == expected


@pytest.mark.parametrize(
    'test_map, expected',
    (
        (m1, (8, 3, 4)),
        (m2, (33, 5, 8)),
        (m3, (35, 1, 2)),
        (m4, (41, 6, 3)),
        (m5, (210, 11, 13)),
    ),
)
def test_find_best_location(test_map, expected):
    assert find_best_location(test_map) == expected


def test_vaporize_from():
    coords = list(vaporize_from(11, 13, m5))
    assert coords[0] == (11, 12)
    assert coords[1] == (12, 1)
    assert coords[2] == (12, 2)
    assert coords[9] == (12, 8)
    assert coords[19] == (16, 0)
    assert coords[49] == (16, 9)
    assert coords[99] == (10, 16)
    assert coords[198] == (9, 6)
    assert coords[199] == (8, 2)
    assert coords[200] == (10, 9)
    assert coords[298] == (11, 1)
    assert coords[-1] == (11, 1)


def test_solve():
    assert solve() == (221, 806)
