# https://adventofcode.com/2019/day/24

from helpers import read_puzzle

type Grid = tuple[tuple[bool, ...], ...]


def parse(s: str) -> Grid:
    return tuple(tuple(ch == '#' for ch in line) for line in s.split())


def update_tile(i: int, j: int, grid: Grid) -> bool:
    bug_count = (
        (i > 0 and grid[i - 1][j])
        + (j > 0 and grid[i][j - 1])
        + (i < 4 and grid[i + 1][j])
        + (j < 4 and grid[i][j + 1])
    )
    return bug_count == 1 or (bug_count == 2 and not grid[i][j])


def update_grid(grid: Grid) -> Grid:
    return tuple(
        tuple(update_tile(i, j, grid) for j in range(5)) for i in range(5)
    )


def calc_bio(grid: Grid) -> int:
    return sum(
        grid[i][j] and 2 ** (i * 5 + j) for i in range(5) for j in range(5)
    )


def part1(grid: Grid) -> int:
    cache = {grid}
    while True:
        grid = update_grid(grid)
        if grid in cache:
            break
        cache.add(grid)
    return calc_bio(grid)


def solve() -> tuple[int, int]:
    grid = parse(read_puzzle())
    return part1(grid), 0


if __name__ == '__main__':
    print(solve())
