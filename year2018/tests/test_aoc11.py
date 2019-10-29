from aoc11 import max_square, power_level, solve, summed_area_table


def test_power_level():
    assert power_level(serial=8, x=3, y=5) == 4
    assert power_level(serial=57, x=122, y=79) == -5
    assert power_level(serial=39, x=217, y=196) == 0
    assert power_level(serial=71, x=101, y=153) == 4


def test_max_square():
    table = summed_area_table(18)
    assert max_square(table, 3) == (29, 33, 45, 3)
    table = summed_area_table(42)
    assert max_square(table, 3) == (30, 21, 61, 3)


def test_solve():
    assert solve() == ((30, 20, 46, 3), (158, 231, 65, 14))
