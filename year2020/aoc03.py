# https://adventofcode.com/2020/day/3

from itertools import count
from math import prod

from helpers import read_puzzle

type Grid = list[list[int]]


def parse(s: str) -> Grid:
    return [[int(char == '#') for char in line] for line in s.split('\n')]


def count_trees(grid: Grid, right: int, down: int) -> int:
    coords = zip(range(0, len(grid), down), count(step=right))
    width = len(grid[0])
    return sum(grid[i][j % width] for i, j in coords)


def solve() -> tuple[int, int]:
    grid = parse(read_puzzle())
    slopes = (1, 1), (3, 1), (5, 1), (7, 1), (1, 2)
    return (
        count_trees(grid, 3, 1),
        prod(count_trees(grid, *slope) for slope in slopes),
    )


if __name__ == '__main__':
    print(solve())
