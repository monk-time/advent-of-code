# https://adventofcode.com/2021/day/9
# tags: #grid #graph-traversal

from collections import defaultdict
from functools import reduce
from operator import mul
from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

type Coord = tuple[int, int]
type Coords = tuple[Coord, ...]
type Grid = dict[Coord, int]


def parse(s: str) -> Grid:
    lines = s.splitlines()
    return {
        (i, j): int(ch)
        for i, line in enumerate(lines)
        for j, ch in enumerate(line)
    }


def around(c: Coord) -> Iterable[Coord]:
    x, y = c
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def find_low_points(g: Grid) -> Coords:
    def is_low(c: Coord) -> bool:
        val = g[c]
        return all(val < g[c2] for c2 in around(c) if c2 in g)

    return tuple(filter(is_low, g))


def calc_risk(g: Grid, low_points: Coords) -> int:
    return sum(g[c] + 1 for c in low_points)


def fill_basins(g: Grid, low_points: Coords) -> int:
    basin_sizes = defaultdict[Coord, int](int)
    visited = set[Coord]()
    for low_point in low_points:
        queue = [low_point]
        while queue:
            c = queue.pop()
            if c in visited:
                continue
            visited.add(c)
            basin_sizes[low_point] += 1
            queue.extend(
                c2 for c2 in around(c) if c2 in g and g[c] < g[c2] < 9
            )
    return reduce(mul, sorted(basin_sizes.values())[-3:])


def solve() -> tuple[int, int]:
    g = parse(read_puzzle())
    low_points = find_low_points(g)
    return calc_risk(g, low_points), fill_basins(g, low_points)


if __name__ == '__main__':
    print(solve())
