from aoc03 import Claim, overlap_and_count, parse, solve, squares

a = parse('#1 @ 1,3: 4x4')
b = parse('#2 @ 3,1: 4x4')
c = parse('#3 @ 5,5: 2x2')


def test_parse():
    assert a.left == 1 and a.width == 4
    assert parse('#123 @ 3,2: 5x4') == Claim(123, 3, 2, 5, 4)
    assert parse('#6 @ 409,863: 17x10') == Claim(6, 409, 863, 17, 10)


def test_squares():
    assert list(squares(c)) == [(5, 5), (5, 6), (6, 5), (6, 6)]


def test_overlap_and_count():
    assert overlap_and_count([a, b, c]) == (4, 3)


def test_solve():
    assert solve() == (110891, 297)
