from string import ascii_letters
from typing import Iterable

from aoc06 import Grid, Point, count_finite, fill_grid, parse_coords
from helpers import read_puzzle

sample = '1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9'
places_ = parse_coords(sample)


def test_parse_coords():
    assert places_ == [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]


def grid_to_str(grid: Grid, places: Iterable[Point], xs: range, ys: range) -> str:
    names = dict(zip(places, ascii_letters))  # 52 points max
    names['.'] = '.'
    names[' '] = ' '
    return '\n'.join(''.join(names[grid.get((i, j), ' ')] for i in xs)
                     for j in ys)


def test_fill_grid():
    grid, xs, ys = fill_grid(places_)
    print()
    print(grid_to_str(grid, places_, xs, ys))
    assert grid_to_str(grid, places_, xs, ys) == '\n'.join([
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


def test_count_finite():
    assert count_finite(places_) == 17


def test_full_puzzle():
    puzzle = read_puzzle()
    places = parse_coords(puzzle)
    assert count_finite(places) == 5626
