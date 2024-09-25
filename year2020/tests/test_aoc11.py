from inspect import cleandoc

import pytest

from year2020.aoc11 import (
    Grid,
    find_loop,
    get_adj_map,
    iterate,
    neighbors_1,
    neighbors_2,
    parse,
    solve,
)

sample1 = cleandoc("""
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
""")

sample2_1 = cleandoc("""
    #.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#
    #.#####.##
""")

sample3_1 = cleandoc("""
    #.LL.L#.##
    #LLLLLL.L#
    L.L.L..L..
    #LLL.LL.L#
    #.LL.LL.LL
    #.LLLL#.##
    ..L.L.....
    #LLLLLLLL#
    #.LLLLLL.L
    #.#LLLL.##
""")

sample4_1 = cleandoc("""
    #.##.L#.##
    #L###LL.L#
    L.#.#..#..
    #L##.##.L#
    #.##.LL.LL
    #.###L#.##
    ..#.#.....
    #L######L#
    #.LL###L.L
    #.#L###.##
""")

sample5_1 = cleandoc("""
    #.#L.L#.##
    #LLL#LL.L#
    L.L.L..#..
    #LLL.##.L#
    #.LL.LL.LL
    #.LL#L#.##
    ..L.L.....
    #L#LLLL#L#
    #.LLLLLL.L
    #.#L#L#.##
""")

sample6_1 = cleandoc("""
    #.#L.L#.##
    #LLL#LL.L#
    L.#.L..#..
    #L##.##.L#
    #.#L.LL.LL
    #.#L#L#.##
    ..L.L.....
    #L#L##L#L#
    #.LLLLLL.L
    #.#L#L#.##
""")

sample2_2 = cleandoc("""
    #.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#
    #.#####.##
""")

sample3_2 = cleandoc("""
    #.LL.LL.L#
    #LLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLL#
    #.LLLLLL.L
    #.LLLLL.L#
""")

sample4_2 = cleandoc("""
    #.L#.##.L#
    #L#####.LL
    L.#.#..#..
    ##L#.##.##
    #.##.#L.##
    #.#####.#L
    ..#.#.....
    LLL####LL#
    #.L#####.L
    #.L####.L#
""")


sample5_2 = cleandoc("""
    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##LL.LL.L#
    L.LL.LL.L#
    #.LLLLL.LL
    ..L.L.....
    LLLLLLLLL#
    #.LLLLL#.L
    #.L#LL#.L#
""")

sample6_2 = cleandoc("""
    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##L#.#L.L#
    L.L#.#L.L#
    #.L####.LL
    ..#.#.....
    LLL###LLL#
    #.LLLLL#.L
    #.L#LL#.L#
""")

sample7_2 = cleandoc("""
    #.L#.L#.L#
    #LLLLLL.LL
    L.L.L..#..
    ##L#.#L.L#
    L.L#.LL.L#
    #.LLLL#.LL
    ..#.L.....
    LLL###LLL#
    #.LLLLL#.L
    #.L#LL#.L#
""")


def grid_to_str(grid: Grid) -> str:
    h = len(grid)
    return '\n'.join(''.join(grid[i]) for i in range(h))


@pytest.mark.parametrize(
    'neighbors, k, grid, next_grid',
    (
        (neighbors_1, 4, sample1, sample2_1),
        (neighbors_1, 4, sample2_1, sample3_1),
        (neighbors_1, 4, sample3_1, sample4_1),
        (neighbors_1, 4, sample4_1, sample5_1),
        (neighbors_1, 4, sample5_1, sample6_1),
        (neighbors_2, 5, sample1, sample2_2),
        (neighbors_2, 5, sample2_2, sample3_2),
        (neighbors_2, 5, sample3_2, sample4_2),
        (neighbors_2, 5, sample4_2, sample5_2),
        (neighbors_2, 5, sample5_2, sample6_2),
        (neighbors_2, 5, sample6_2, sample7_2),
    ),
)
def test_iterate(neighbors, k, grid, next_grid):
    grid = parse(grid)
    adj_map = get_adj_map(grid, neighbors)
    assert grid_to_str(iterate(grid, adj_map, k)) == next_grid


def test_find_loop():
    assert find_loop(parse(sample1), neighbors_1, 4) == 37
    assert find_loop(parse(sample1), neighbors_2, 5) == 26


def test_solve():
    assert solve() == (2299, 2047)
