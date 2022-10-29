from year2019.aoc08 import split_into_layers, solve, decode_pixel, decode_image


def test_split_into_layers():
    assert split_into_layers('123456789012', 6) == ['123456', '789012']


def test_decode_pixel():
    assert decode_pixel('2201') == '0'
    assert decode_pixel('1220') == '1'


def test_decode_image():
    assert ''.join(decode_image('0222112222120000', 2, 2)) == '0110'


def test_solve():
    assert solve() == (2480, 0)
