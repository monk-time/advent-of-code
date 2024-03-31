# https://adventofcode.com/2018/day/11

from itertools import product
from multiprocessing import Pool

from helpers import read_puzzle

GRID = 300


def power_level(serial: int, x: int, y: int) -> int:
    return ((x + 10) * y + serial) * (x + 10) // 100 % 10 - 5


Table = list[list[int]]


def summed_area_table(serial: int) -> Table:
    t = [[0] * (GRID + 1)]
    for x in range(1, GRID + 1):
        t.append([0])
        for y in range(1, GRID + 1):
            t[x].append(
                power_level(serial, x, y)
                + t[x][y - 1]
                + t[x - 1][y]
                - t[x - 1][y - 1]
            )
    return t


def max_square(t: Table, size: int):
    max_ = (float('-inf'), 0, 0, 0)
    for x, y in product(range(size, GRID + 1), repeat=2):
        power = (
            t[x][y] - t[x][y - size] - t[x - size][y] + t[x - size][y - size]
        )
        if power > max_[0]:
            max_ = (power, x - size + 1, y - size + 1, size)
    return max_


def max_square_any_size(t: Table):
    return max(max_square(t, size + 1) for size in range(GRID))


def max_square_any_size_parallel(t: Table):
    with Pool(processes=4) as p:
        res = p.starmap(max_square, ((t, size + 1) for size in range(GRID)))
    return max(res)


def solve():
    table = summed_area_table(int(read_puzzle()))
    return max_square(table, 3), max_square_any_size_parallel(table)


if __name__ == '__main__':
    print(solve())
