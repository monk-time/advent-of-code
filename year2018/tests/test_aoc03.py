from aoc03 import Claim, claim_to_points, solve, parse, overlap
from helpers import read_puzzle

a = parse('#1 @ 1,3: 4x4')
b = parse('#2 @ 3,1: 4x4')
c = parse('#3 @ 5,5: 2x2')


def test_parse():
    assert a.left == 1 and a.width == 4
    assert parse('#123 @ 3,2: 5x4') == Claim(123, 3, 2, 5, 4)
    assert parse('#6 @ 409,863: 17x10') == Claim(6, 409, 863, 17, 10)


def test_overlap():
    assert overlap(a, b) == Claim((1, 2), 3, 3, 2, 2)
    assert overlap(b, a) == Claim((2, 1), 3, 3, 2, 2)
    assert overlap(a, c) is None
    assert overlap(b, c) is None


def test_claim_to_points():
    assert list(claim_to_points(c)) == [(5, 5), (5, 6), (6, 5), (6, 6)]


def test_solve():
    assert solve([a, b, c]) == (4, 3)


def test_full_puzzle():
    puzzle = [parse(line) for line in read_puzzle().splitlines()]
    assert solve(puzzle) == (110891, 297)
