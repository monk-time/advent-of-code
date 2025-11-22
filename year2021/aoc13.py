# https://adventofcode.com/2021/day/13
# tags: #grid #instructions

import re
from functools import reduce
from itertools import batched
from typing import cast

from utils_proxy import read_puzzle

type Coord = tuple[int, int]
type Coords = tuple[Coord, ...]
type Grid = set[Coord]


def parse(s: str) -> tuple[Grid, Coords]:
    s1, s2 = s.split('\n\n')
    s2 = re.sub(r'x=(\d+)', r'\1,0', s2)
    s2 = re.sub(r'y=(\d+)', r'0,\1', s2)
    grid = set(batched(map(int, re.findall(r'\d+', s1)), 2, strict=True))
    folds = tuple(batched(map(int, re.findall(r'\d+', s2)), 2, strict=True))
    return cast('Grid', grid), cast('Coords', folds)


def fold(grid: Grid, fold: Coord) -> Grid:
    # Assuming folds are always in the middle
    x_f, y_f = fold
    return {
        (min(x, abs(2 * x_f - x)), min(y, abs(2 * y_f - y)))
        for x, y in grid
        if fold not in {(x, 0), (0, y)}
    }


def fold_all(grid: Grid, folds: Coords) -> Grid:
    return reduce(fold, folds, grid)


def grid_to_str(grid: Grid) -> str:
    x_max, y_max = map(max, zip(*grid))
    return '\n'.join(
        ''.join(' █'[(x, y) in grid] for x in range(x_max + 1))
        for y in range(y_max + 1)
    )


def solve() -> tuple[int, int]:
    grid, folds = parse(read_puzzle())
    final_grid = fold_all(grid, folds)
    print(grid_to_str(final_grid))
    return len(fold(grid, folds[0])), len(final_grid)


if __name__ == '__main__':
    print(solve())
