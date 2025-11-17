from inspect import cleandoc

import pytest

from year2021.aoc09 import (
    Coords,
    Grid,
    calc_risk,
    fill_basins,
    find_low_points,
    parse,
    solve,
)

sample = cleandoc("""
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678
""")


@pytest.fixture(scope='module')
def sample_grid() -> Grid:
    return parse(sample)


@pytest.fixture(scope='module')
def sample_low_points(sample_grid: Grid) -> Coords:
    return find_low_points(sample_grid)


def test_calc_risk(sample_grid: Grid, sample_low_points: Coords):
    assert calc_risk(sample_grid, sample_low_points) == 15


def test_fill_basins(sample_grid: Grid, sample_low_points: Coords):
    assert fill_basins(sample_grid, sample_low_points) == 1134


def test_solve():
    assert solve() == (439, 900900)
