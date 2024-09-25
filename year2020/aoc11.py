# https://adventofcode.com/2020/day/11

from collections.abc import Callable, Iterable
from itertools import product

from helpers import read_puzzle

type Coord = tuple[int, int]
type Grid = tuple[tuple[str, ...], ...]
type AdjMap = dict[Coord, tuple[Coord, ...]]
type NeighborFunc = Callable[[Coord, Grid], Iterable[Coord]]


def parse(s: str) -> Grid:
    return tuple(tuple(line) for line in s.split('\n'))


def neighbors_1(c: Coord, grid: Grid) -> Iterable[Coord]:
    h, w = len(grid), len(grid[0])
    i, j = c
    for di, dj in product(range(-1, 2), repeat=2):
        if di == dj == 0:
            continue
        i2, j2 = i + di, j + dj
        if not (0 <= i2 < h and 0 <= j2 < w) or grid[i2][j2] == '.':
            continue
        yield (i2, j2)


def neighbors_2(c: Coord, grid: Grid) -> Iterable[Coord]:
    h, w = len(grid), len(grid[0])
    i, j = c
    for di, dj in product(range(-1, 2), repeat=2):
        if di == dj == 0:
            continue
        i2, j2 = i, j
        while 0 <= (i2 := i2 + di) < h and 0 <= (j2 := j2 + dj) < w:
            if grid[i2][j2] != '.':
                yield (i2, j2)
                break


def get_adj_map(grid: Grid, neighbors: NeighborFunc) -> AdjMap:
    h, w = len(grid), len(grid[0])
    return {c: tuple(neighbors(c, grid)) for c in product(range(h), range(w))}


def update_seat(i: int, j: int, grid: Grid, adj_map: AdjMap, k: int) -> str:
    if (seat := grid[i][j]) == '.':
        return '.'
    occupied_count = 0
    for i2, j2 in adj_map[i, j]:
        occupied_count += grid[i2][j2] == '#'
        if (seat == 'L' and occupied_count > 0) or occupied_count == k:
            return 'L'
    return '#'


def iterate(grid: Grid, adj_map: AdjMap, k: int) -> Grid:
    h, w = len(grid), len(grid[0])
    return tuple(
        tuple(update_seat(i, j, grid, adj_map, k) for j in range(w))
        for i in range(h)
    )


def find_loop(grid: Grid, neighbors: NeighborFunc, k: int) -> int:
    adj_map = get_adj_map(grid, neighbors)
    cache: set[Grid] = set()
    while grid not in cache:
        cache.add(grid)
        grid = iterate(grid, adj_map, k)
    return sum(grid[i].count('#') for i in range(len(grid)))


def solve() -> tuple[int, int]:
    grid = parse(read_puzzle())
    return (
        find_loop(grid, neighbors_1, 4),
        find_loop(grid, neighbors_2, 5),
    )


if __name__ == '__main__':
    print(solve())
