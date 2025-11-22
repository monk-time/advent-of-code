# https://adventofcode.com/2018/day/6

import re
from collections import Counter
from itertools import product
from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

Point = tuple[int, int]
Grid = dict[Point, Point | str]


def parse_coords(s: str) -> list[Point]:
    return [
        tuple(map(int, re.findall(r'\d+', line))) for line in s.splitlines()
    ]  # type: ignore


def grid_size(points: Iterable[Point]) -> tuple[range, range]:
    """Find the miminum area that contains all points."""

    def get_range(arr: list[int]) -> range:
        return range(min(arr), max(arr) + 1)

    p_xs = [x for x, _ in points]
    p_ys = [y for _, y in points]
    return get_range(p_xs), get_range(p_ys)


def closest(points: Iterable[Point], p: Point) -> Point | str:
    dists = (abs(p[0] - x) + abs(p[1] - y) for x, y in points)
    (d1, p1), (d2, _p2), *_ = sorted(zip(dists, points))
    return p1 if d1 < d2 else '.'


def fill_grid(points: Iterable[Point]) -> Grid:
    xs, ys = grid_size(points)
    return {p: closest(points, p) for p in product(xs, ys)}


def largest_finite(points: Iterable[Point]) -> int:
    grid = fill_grid(points)
    xs, ys = grid_size(points)
    edge = (
        {grid[x, ys[0]] for x in xs}
        | {grid[xs[0], y] for y in ys}
        | {grid[x, ys[-1]] for x in xs}
        | {grid[xs[-1], y] for y in ys}
    )
    counter = Counter(p for p in grid.values() if p not in edge)
    return counter.most_common(1)[0][1]


def safe_region(points: Iterable[Point], max_sum: int) -> int:
    xs, ys = grid_size(points)
    return sum(
        sum(abs(x - px) + abs(y - py) for px, py in points) < max_sum
        for x in xs
        for y in ys
    )


def solve():
    points = parse_coords(read_puzzle())
    return largest_finite(points), safe_region(points, 10000)


if __name__ == '__main__':
    print(solve())
