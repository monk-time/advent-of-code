from inspect import cleandoc

import pytest

from year2020.aoc13 import (
    chinese_remainder_theorem,
    earliest_bus,
    parse,
    solve,
)

sample_1 = cleandoc("""
    939
    7,13,x,x,59,x,31,19
""")


def test_earliest_bus():
    n, nums, _ = parse(sample_1)
    assert earliest_bus(n, nums) == 295


@pytest.mark.parametrize(
    'sample, result',
    (
        (sample_1, 1068781),
        ('0\n17,x,13,19', 3417),
        ('0\n67,7,59,61', 754018),
        ('0\n67,x,7,59,61', 779210),
        ('0\n67,7,x,59,61', 1261476),
        ('0\n1789,37,47,1889', 1202161486),
    ),
)
def test_chinese_remainder_theorem(sample: str, result: int):
    _, nums, remainders = parse(sample)
    assert chinese_remainder_theorem(nums, remainders) == result


def test_solve():
    assert solve() == (6559, 626670513163231)
