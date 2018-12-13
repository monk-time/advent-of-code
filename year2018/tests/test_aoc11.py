from aoc11 import GRID, max_square_any_size, \
    max_square_quick, max_square_summed_area, power_level, summed_area_table
from helpers import read_puzzle


def test_power_level():
    assert power_level(serial=8, x=3, y=5) == 4
    assert power_level(serial=57, x=122, y=79) == -5
    assert power_level(serial=39, x=217, y=196) == 0
    assert power_level(serial=71, x=101, y=153) == 4


def test_max_square_by_columns():
    table = summed_area_table(18)
    assert max_square_summed_area(table, 3, 3) == (29, 33, 45, 3)
    table = summed_area_table(42)
    assert max_square_summed_area(table, 3, 3) == (30, 21, 61, 3)


def test_full_puzzle():
    table = summed_area_table(int(read_puzzle()))
    assert max_square_summed_area(table, 3, 3) == (30, 20, 46, 3)
    assert max_square_quick(table, 3) == (30, 20, 46, 3)
    assert max_square_summed_area(table, 1, GRID) == (158, 231, 65, 14)
    assert max_square_any_size(table) == (158, 231, 65, 14)
