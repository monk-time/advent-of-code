from inspect import cleandoc
from math import sqrt

from year2021.aoc11 import (
    Grid,
    count_flashes,
    find_synchro_step,
    parse,
    solve,
    step,
)

sample_small = cleandoc("""
    11111
    19991
    19191
    19991
    11111
""")

sample = cleandoc("""
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526
""")


def grid_to_str(grid: Grid) -> str:
    n = int(sqrt(len(grid)))  # assuming the grid is always a square
    return '\n'.join(
        ''.join(str(grid[i, j]) for j in range(n)) for i in range(n)
    )


def test_step():
    grid = parse(sample_small)
    grid, _ = step(grid)
    assert grid_to_str(grid) == cleandoc("""
        34543
        40004
        50005
        40004
        34543
    """)


def test_count_flashes():
    grid = parse(sample)
    assert count_flashes(grid, 10) == 204
    assert count_flashes(grid, 100) == 1656


def test_find_synchro_step():
    assert find_synchro_step(parse(sample)) == 195


def test_solve():
    assert solve() == (1652, 220)
