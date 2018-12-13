from functools import lru_cache
from itertools import product

from helpers import read_puzzle, timed


@lru_cache(maxsize=None)
def power_level(serial: int, x: int, y: int) -> int:
    return ((x + 10) * y + serial) * (x + 10) // 100 % 10 - 5


def total_power(serial: int, x: int, y: int) -> int:
    return sum(power_level(serial, x + dx, y + dy)
               for dx, dy in product(range(3), repeat=2))


@timed
def max_square(serial: int):
    key = lambda coords: total_power(serial, *coords)
    x, y = max(product(range(1, 299), repeat=2), key=key)
    return f'{x},{y}'


if __name__ == '__main__':
    serial_ = int(read_puzzle())
    print(max_square(serial_))
