from typing import List

from aoc11 import max_square_any_size, max_square_by_columns, max_square_naive, power_level
from helpers import read_puzzle


def segment(serial: int, x: int, y: int, size: int) -> List[str]:
    return [' '.join(f'{power_level(serial, x + dx, y + dy):4d}' for dx in range(size))
            for dy in range(size)]


def test_power_level():
    assert power_level(serial=8, x=3, y=5) == 4
    assert power_level(serial=57, x=122, y=79) == -5
    assert power_level(serial=39, x=217, y=196) == 0
    assert power_level(serial=71, x=101, y=153) == 4


def test_max_square_naive():
    assert max_square_naive(18) == (29, 33, 45, 3)
    assert max_square_naive(42) == (30, 21, 61, 3)


def test_max_square_by_columns():
    assert max_square_by_columns(18) == (29, 33, 45, 3)
    assert max_square_by_columns(42) == (30, 21, 61, 3)


def test_full_puzzle():
    serial = int(read_puzzle())
    assert max_square_naive(serial) == (30, 20, 46, 3)
    assert max_square_any_size(serial) == (158, 231, 65, 14)
