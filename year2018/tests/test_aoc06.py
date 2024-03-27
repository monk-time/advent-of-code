from collections.abc import Iterable
from string import ascii_letters

from year2018.aoc06 import (
    Grid,
    Point,
    fill_grid,
    grid_size,
    largest_finite,
    parse_coords,
    safe_region,
    solve,
)

sample = '1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9'
points_ = parse_coords(sample)


def test_parse_coords():
    assert points_ == [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]


def test_grid_size():
    assert grid_size(points_) == (range(1, 9), range(1, 10))


def grid_to_str(grid: Grid, points: Iterable[Point]) -> str:
    # max 52 points
    names: dict[Point | str, str] = dict(zip(points, ascii_letters))
    names['.'] = '.'
    names[' '] = ' '
    xs, ys = grid_size(points)
    return '\n'.join(
        ''.join(names[grid.get((i, j), ' ')] for i in xs) for j in ys
    )


def test_fill_grid():
    grid = fill_grid(points_)
    assert grid_to_str(grid, points_) == '\n'.join([
        'aaaa.ccc',
        'aaddeccc',
        'adddeccc',
        '.dddeecc',
        'b.deeeec',
        'bb.eeee.',
        'bb.eeeff',
        'bb.eefff',
        'bb.fffff',
    ])


def test_largest_finite():
    assert largest_finite(points_) == 17


def test_safe_region():
    assert safe_region(points_, 32) == 16


def test_solve():
    assert solve() == (5626, 46554)
