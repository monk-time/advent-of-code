from year2021.aoc07 import (
    calc_fuel,
    get_total_fuel,
    get_total_fuel_2,
    parse,
    solve,
)

sample = '16,1,2,0,4,2,7,1,2,14'


def test_calc_fuel():
    assert calc_fuel(parse(sample), get_total_fuel) == 37
    assert calc_fuel(parse(sample), get_total_fuel_2) == 168


def test_solve():
    assert solve() == (344605, 93699985)
