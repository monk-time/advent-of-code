from string import ascii_letters
from typing import Iterable

from aoc06 import Grid, Point, count_finite, fill_grid, get_ranges, parse_coords, safe_region
from helpers import read_puzzle

sample = '1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9'
places_ = parse_coords(sample)


def test_parse_coords():
    assert places_ == [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]


def test_get_ranges():
    assert get_ranges(places_) == (range(1, 9), range(1, 10))


def grid_to_str(grid: Grid, places: Iterable[Point]) -> str:
    names = dict(zip(places, ascii_letters))  # 52 points max
    names['.'] = '.'
    names[' '] = ' '
    xs, ys = get_ranges(places)
    return '\n'.join(''.join(names[grid.get((i, j), ' ')] for i in xs)
                     for j in ys)


def test_fill_grid():
    grid = fill_grid(places_)
    assert grid_to_str(grid, places_) == '\n'.join([
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


def test_safe_region():
    assert safe_region(places_, 32) == 16


def test_full_puzzle():
    places = parse_coords(read_puzzle())
    assert count_finite(places) == 5626
    assert safe_region(places, 10000) == 46554
