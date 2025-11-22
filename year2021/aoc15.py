# https://adventofcode.com/2021/day/15
# tags: #grid #graph-traversal #dijkstra

import heapq
import math
from collections import defaultdict

from utils_proxy import read_puzzle

type Coord = tuple[int, int]
type Grid = dict[Coord, int]


def parse(s: str) -> Grid:
    return {
        (i, j): int(ch)
        for i, line in enumerate(s.splitlines())
        for j, ch in enumerate(line)
    }


def find_min_path(grid: Grid) -> int:
    source = (0, 0)
    target: Coord = tuple(map(max, zip(*grid)))
    dist = defaultdict[Coord, float](lambda: math.inf)
    queue: list[tuple[float, Coord]] = [(0, source)]
    dist[source] = 0
    while queue:
        c = x, y = heapq.heappop(queue)[1]
        if c == target:
            break
        for c2 in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)):
            if c2 not in grid:
                continue
            if (alt := dist[c] + grid[c2]) < dist[c2]:
                dist[c2] = alt
                heapq.heappush(queue, (alt, c2))
    return int(dist[target])


def expand(grid: Grid) -> Grid:
    h, w = tuple(int(max(arr)) + 1 for arr in zip(*grid))
    return {
        (tile_i * h + i, tile_j * w + j): (val + tile_i + tile_j - 1) % 9 + 1
        for (i, j), val in grid.items()
        for tile_i in range(5)
        for tile_j in range(5)
    }


def solve() -> tuple[int, int]:
    grid = parse(read_puzzle())
    return find_min_path(grid), find_min_path(expand(grid))


if __name__ == '__main__':
    print(solve())
