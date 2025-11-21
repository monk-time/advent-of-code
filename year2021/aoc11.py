# https://adventofcode.com/2021/day/11
# tags: #grid #graph-traversal

from functools import cache
from itertools import count, product
from typing import cast

from helpers import read_puzzle

type Coord = tuple[int, int]
type Coords = tuple[Coord, ...]
type Grid = dict[Coord, int]


def parse(s: str) -> Grid:
    return {
        (i, j): int(ch)
        for i, line in enumerate(s.splitlines())
        for j, ch in enumerate(line)
    }


@cache
def around(c: Coord) -> Coords:
    return tuple(
        cast('Coord', tuple(c[i] + delta[i] for i in range(2)))
        for delta in product(range(-1, 2), repeat=len(c))
        if not all(i == 0 for i in delta)
    )


def step(base_gird: Grid) -> tuple[Grid, int]:
    flash_queue, count = set[Coord](), 0
    grid: Grid = {}
    for c in base_gird:
        grid[c] = base_gird[c] + 1
        if grid[c] > 9:
            flash_queue.add(c)
    while flash_queue:
        flash = flash_queue.pop()
        grid[flash] = 0
        count += 1
        for c in around(flash):
            if c not in grid or grid[c] == 0:
                continue
            grid[c] += 1
            if grid[c] > 9:
                flash_queue.add(c)
    return grid, count


def count_flashes(grid: Grid, steps: int) -> int:
    total = 0
    for _ in range(steps):
        grid, flashes = step(grid)
        total += flashes
    return total


def find_synchro_step(grid: Grid) -> int:
    for i in count(1):
        grid, flashes = step(grid)
        if flashes == len(grid):
            return i
    return 0


def solve() -> tuple[int, int]:
    grid = parse(read_puzzle())
    return count_flashes(grid, 100), find_synchro_step(grid)


if __name__ == '__main__':
    print(solve())
