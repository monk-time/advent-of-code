import multiprocessing
from collections import deque
from functools import lru_cache
from itertools import product

from helpers import read_puzzle, timed

GRID = 300


@lru_cache(maxsize=None)
def power_level(serial: int, x: int, y: int) -> int:
    return ((x + 10) * y + serial) * (x + 10) // 100 % 10 - 5


def total_power(serial: int, x: int, y: int, size: int) -> int:
    return sum(power_level(serial, x + dx, y + dy)
               for dx, dy in product(range(size), repeat=2))


@timed
def max_square_naive(serial: int, size: int = 3):
    """Find the maximum power by recalculating every square afresh."""
    corners = product(range(1, GRID + 2 - size), repeat=2)
    return max((total_power(serial, *c, size), *c, size) for c in corners)


def max_square_by_columns(serial: int, size: int = 3):
    """Find the maximum power by moving a square in a LTR-then-TTB direction.

    On each horizontal pass a square is cached and moved column by column."""
    column = lambda i, j: sum(power_level(serial, i, j + d) for d in range(size))
    max_power, max_coords = float('-inf'), (1, 1)
    for y in range(1, GRID + 2 - size):
        # A square is represented by a list of totals of its columns
        square = deque(column(1 + d, y) for d in range(size))
        power = sum(square)
        if power > max_power:
            max_power, max_coords = power, (1, y)
        for x in range(size + 1, GRID + 1):
            # Add a new column and check if the total has increased
            c_old = square.popleft()
            c_new = column(x, y)
            square.append(c_new)
            power += c_new - c_old
            if power > max_power:
                max_power, max_coords = power, (x - size + 1, y)
    return (max_power, *max_coords, size)


@timed
def max_square_any_size(serial: int):
    with multiprocessing.Pool(8) as p:
        res = p.starmap(max_square_by_columns, ((serial, size) for size in range(1, GRID + 1)))
    return max(res)


if __name__ == '__main__':
    serial_ = int(read_puzzle())
    print(max_square_naive(serial_))
    print(max_square_any_size(serial_))
