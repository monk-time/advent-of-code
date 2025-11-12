from year2020.aoc25 import find_lsize, get_enc_key, solve


def test_find_lsize():
    assert find_lsize(5764801) == 8
    assert find_lsize(17807724) == 11


def test_get_enc_key():
    assert get_enc_key(5764801, 17807724) == 14897079


def test_solve():
    assert solve() == (9714832, 0)
