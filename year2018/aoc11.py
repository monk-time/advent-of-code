from collections import defaultdict
from itertools import product
from multiprocessing import Pool
from typing import Dict, Tuple

from helpers import print_peak_memory_used, read_puzzle, timed

GRID = 300


def power_level(serial: int, x: int, y: int) -> int:
    return ((x + 10) * y + serial) * (x + 10) // 100 % 10 - 5


Table = Dict[Tuple[int, int], int]


def summed_area_table(serial: int) -> Table:
    t = defaultdict(int)
    for x, y in product(range(1, GRID + 1), repeat=2):
        t[(x, y)] = power_level(serial, x, y) + \
                    t[(x, y - 1)] + t[(x - 1, y)] - t[(x - 1, y - 1)]
    return t


@timed
def max_square_summed_area(t: Table, min_size: int, max_size: int):
    max_square = (float('-inf'), 0, 0, 0)
    for s in range(min_size, max_size + 1):
        for x, y in product(range(s, GRID + 1), repeat=2):
            power = t[(x, y)] - t[(x, y - s)] - t[(x - s, y)] + t[(x - s, y - s)]
            if power > max_square[0]:
                max_square = (power, x - s + 1, y - s + 1, s)
    return max_square


def max_square_quick(t: Table, size: int):
    max_square = (float('-inf'), 0, 0, 0)
    for x, y in product(range(size, GRID + 1), repeat=2):
        power = t[(x, y)] - t[(x, y - size)] - t[(x - size, y)] + t[(x - size, y - size)]
        if power > max_square[0]:
            max_square = (power, x - size + 1, y - size + 1, size)
    return max_square


@timed
def max_square_any_size(t: Table):
    with Pool(4) as p:
        res = p.starmap(max_square_quick,
                        ((t, size + 1) for size in range(GRID)))
    return max(res)


if __name__ == '__main__':
    table = summed_area_table(int(read_puzzle()))
    print(max_square_summed_area(table, 3, 3))
    print(max_square_quick(table, 3))
    print(max_square_summed_area(table, 1, GRID))
    print(max_square_any_size(table))
    print_peak_memory_used()
