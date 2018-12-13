from aoc11 import max_square, power_level
from helpers import read_puzzle


def test_power_level():
    assert power_level(serial=8, x=3, y=5) == 4
    assert power_level(serial=57, x=122, y=79) == -5
    assert power_level(serial=39, x=217, y=196) == 0
    assert power_level(serial=71, x=101, y=153) == 4


def test_max_square():
    assert max_square(18) == '33,45'
    assert max_square(42) == '21,61'


def test_full_puzzle():
    serial = int(read_puzzle())
    assert max_square(serial) == '20,46'
