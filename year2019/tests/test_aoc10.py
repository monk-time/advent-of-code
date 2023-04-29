from inspect import cleandoc

from ..aoc10 import count_visible_from, find_best_location, parse, solve, vaporize_from

m1 = parse(cleandoc("""
    .#..#
    .....
    #####
    ....#
    ...##
"""))

m2 = parse(cleandoc("""
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
"""))

m3 = parse(cleandoc("""
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
"""))

m4 = parse(cleandoc("""
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
"""))

m5 = parse(cleandoc("""
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
"""))


def test_count_visible_from():
    assert count_visible_from(1, 0, m1) == 7
    assert count_visible_from(4, 0, m1) == 7
    assert count_visible_from(0, 2, m1) == 6
    assert count_visible_from(1, 2, m1) == 7
    assert count_visible_from(2, 2, m1) == 7
    assert count_visible_from(3, 2, m1) == 7
    assert count_visible_from(4, 2, m1) == 5
    assert count_visible_from(4, 3, m1) == 7
    assert count_visible_from(3, 4, m1) == 8
    assert count_visible_from(4, 4, m1) == 7


def test_find_best_location():
    assert find_best_location(m1) == (8, 3, 4)
    assert find_best_location(m2) == (33, 5, 8)
    assert find_best_location(m3) == (35, 1, 2)
    assert find_best_location(m4) == (41, 6, 3)
    assert find_best_location(m5) == (210, 11, 13)


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
