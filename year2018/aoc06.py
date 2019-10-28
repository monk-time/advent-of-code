import re
from collections import Counter
from itertools import product
from typing import Dict, Iterable, List, Tuple, Union

from helpers import read_puzzle

Point = Tuple[int, int]
Grid = Dict[Point, Union[Point, str]]


def parse_coords(s: str) -> List[Point]:
    return [tuple(map(int, re.findall(r'\d+', l))) for l in s.splitlines()]


def grid_size(points: Iterable[Point]) -> Tuple[range, range]:
    """Find the miminum area that contains all points."""
    p_xs = [x for x, _ in points]
    p_ys = [y for _, y in points]
    get_range = lambda arr: range(min(arr), max(arr) + 1)
    return get_range(p_xs), get_range(p_ys)


def closest(points: Iterable[Point], p: Point) -> Union[Point, str]:
    dists = (abs(p[0] - x) + abs(p[1] - y) for x, y in points)
    (d1, p1), (d2, p2), *_ = sorted(zip(dists, points))
    return p1 if d1 < d2 else '.'


def fill_grid(points: Iterable[Point]) -> Grid:
    xs, ys = grid_size(points)
    return dict((p, closest(points, p)) for p in product(xs, ys))


def largest_finite(points: Iterable[Point]) -> int:
    grid = fill_grid(points)
    xs, ys = grid_size(points)
    edge = (set(grid[x, ys[0]] for x in xs) |
            set(grid[xs[0], y] for y in ys) |
            set(grid[x, ys[-1]] for x in xs) |
            set(grid[xs[-1], y] for y in ys))
    return Counter(p for p in grid.values() if p not in edge).most_common(1)[0][1]


def safe_region(points: Iterable[Point], max_sum: int) -> int:
    xs, ys = grid_size(points)
    return sum(sum(abs(x - px) + abs(y - py) for px, py in points) < max_sum
               for x in xs for y in ys)


def solve():
    points = parse_coords(read_puzzle())
    return largest_finite(points), safe_region(points, 10000)


if __name__ == '__main__':
    print(solve())
