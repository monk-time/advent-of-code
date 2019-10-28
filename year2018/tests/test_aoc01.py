from aoc01 import calibrate, calibrate_until_repeat, parse, solve


def test_parse():
    assert list(parse('+1')) == [1]
    assert list(parse('+1, -2, +3')) == [1, -2, 3]
    assert list(parse('+1\n-2\n+3')) == [1, -2, 3]


def test_calibrate_basic():
    assert calibrate('+1') == 1
    assert calibrate('-2', 1) == -1
    assert calibrate('+3', -1) == 2
    assert calibrate('+1', 2) == 3


def test_calibrate_main_example():
    assert calibrate('+1, -2, +3, +1') == 3


def test_calibrate_other_sequences():
    assert calibrate('+1, +1, +1') == 3
    assert calibrate('+1, +1, -2') == 0
    assert calibrate('-1, -2, -3') == -6


def test_calibrate_until_repeat_main():
    assert calibrate_until_repeat('+1, -2, +3, +1') == 2


def test_calibrate_until_repeat_other():
    assert calibrate_until_repeat('+1, -1') == 0
    assert calibrate_until_repeat('+3, +3, +4, -2, -4') == 10
    assert calibrate_until_repeat('-6, +3, +8, +5, -6') == 5
    assert calibrate_until_repeat('+7, +7, -2, -7, -4') == 14


def test_solve():
    assert solve() == (592, 241)
