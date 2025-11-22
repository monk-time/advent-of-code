# https://adventofcode.com/2021/day/7
# tags: #early-exit #triangular-numbers

from itertools import pairwise
from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Callable

type Nums = tuple[int, ...]


def parse(s: str) -> Nums:
    return tuple(int(x) for x in s.split(','))


def get_total_fuel(nums: Nums, dest: int) -> int:
    return sum(abs(n - dest) for n in nums)


def get_total_fuel_2(nums: Nums, dest: int) -> int:
    return sum(abs(n - dest) * (abs(n - dest) + 1) // 2 for n in nums)


def calc_fuel(nums: Nums, fuel_func: Callable[[Nums, int], int]) -> int:
    nums = tuple(sorted(nums))
    dists = (fuel_func(nums, dest) for dest in range(nums[0], nums[-1] + 1))
    return next(d1 for d1, d2 in pairwise(dists) if d1 < d2)


def solve() -> tuple[int, int]:
    nums = parse(read_puzzle())
    return calc_fuel(nums, get_total_fuel), calc_fuel(nums, get_total_fuel_2)


if __name__ == '__main__':
    print(solve())
