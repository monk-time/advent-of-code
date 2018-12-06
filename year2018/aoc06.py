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


def closest(places: Iterable[Point], p: Point) -> Union[Point, str]:
    dists = (abs(p[0] - x) + abs(p[1] - y) for x, y in places)
    (d1, p1), (d2, p2), *_ = sorted(zip(dists, places))
    return p1 if d1 < d2 else '.'


def fill_grid(places: Iterable[Point]) -> Tuple[Grid, range, range]:
    p_xs = [x for x, _ in places]
    p_ys = [y for _, y in places]
    xs = range(min(p_xs), max(p_xs) + 1)
    ys = range(min(p_ys), max(p_ys) + 1)
    return dict((p, closest(places, p)) for p in product(xs, ys)), xs, ys


def count_finite(places: Iterable[Point]):
    grid, xs, ys = fill_grid(places)
    edge = (set(grid[x, ys[0]] for x in xs) |
            set(grid[x, ys[-1]] for x in xs) |
            set(grid[xs[0], y] for y in ys) |
            set(grid[xs[-1], y] for y in ys))
    return Counter(p for p in grid.values() if p not in edge).most_common(1)[0][1]


if __name__ == '__main__':
    # puzzle = '1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9'
    puzzle = read_puzzle()
    places_ = parse_coords(puzzle)
    print(count_finite(places_))
