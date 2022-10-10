from year2019.aoc01 import fuel, fuel_req, solve


def test_fuel():
    assert fuel(12) == 2
    assert fuel(14) == 2
    assert fuel(1969) == 654
    assert fuel(100756) == 33583


def test_fuel_req():
    assert fuel_req(14) == 2
    assert fuel_req(1969) == 966
    assert fuel_req(100756) == 50346


def test_solve():
    assert solve() == (3256599, 4882038)
