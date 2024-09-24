from year2020.aoc09 import find_contiguous_sum, find_invalid, solve

sample = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]


def test_find_invalid():
    assert find_invalid(sample, 5) == 127


def test_find_contiguos_sum():
    assert find_contiguous_sum(sample, 127) == 62


def test_solve():
    assert solve() == (3199139634, 438559930)
