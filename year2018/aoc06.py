import re
from collections import Counter
from itertools import product
from typing import Dict, Iterable, List, Tuple, Union

from helpers import read_puzzle

Point = Tuple[int, int]
Grid = Dict[Point, Union[Point, str]]


def parse_coords(s: str) -> List[Point]:
    res: List[Point] = [tuple(map(int, re.findall(r'\d+', p))) for p in s.splitlines()]
    return res


def get_ranges(places) -> Tuple[range, range]:
    p_xs = [x for x, _ in places]
    p_ys = [y for _, y in places]
    xs = range(min(p_xs), max(p_xs) + 1)
    ys = range(min(p_ys), max(p_ys) + 1)
    return xs, ys


def closest(places: Iterable[Point], p: Point) -> Union[Point, str]:
    dists = (abs(p[0] - x) + abs(p[1] - y) for x, y in places)
    (d1, p1), (d2, p2), *_ = sorted(zip(dists, places))
    return p1 if d1 < d2 else '.'


def fill_grid(places: Iterable[Point]) -> Grid:
    xs, ys = get_ranges(places)
    return dict((p, closest(places, p)) for p in product(xs, ys))


def count_finite(places: Iterable[Point]) -> int:
    grid = fill_grid(places)
    xs, ys = get_ranges(places)
    edge = (set(grid[x, ys[0]] for x in xs) |
            set(grid[xs[0], y] for y in ys) |
            set(grid[x, ys[-1]] for x in xs) |
            set(grid[xs[-1], y] for y in ys))
    return Counter(p for p in grid.values() if p not in edge).most_common(1)[0][1]


def safe_region(places: Iterable[Point], max_sum: int) -> int:
    xs, ys = get_ranges(places)
    return sum(sum(abs(x - px) + abs(y - py) for px, py in places) < max_sum
               for x in xs for y in ys)


if __name__ == '__main__':
    puzzle = read_puzzle()
    places_ = parse_coords(puzzle)
    print(count_finite(places_))
    print(safe_region(places_, 10000))
