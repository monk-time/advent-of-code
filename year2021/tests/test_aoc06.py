from year2021.aoc06 import grow, parse, solve

sample = '3,4,3,1,2'


def test_grow():
    nums = parse(sample)
    assert grow(nums, 18) == 26
    assert grow(nums, 80) == 5934
    assert grow(nums, 256) == 26984457539


def test_solve():
    assert solve() == (390923, 1749945484935)
