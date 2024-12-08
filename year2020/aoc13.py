# https://adventofcode.com/2020/day/13


from math import prod

from helpers import read_puzzle

type Numbers = tuple[int, ...]


def parse(s: str) -> tuple[int, Numbers, Numbers]:
    n, line = s.split('\n')
    arr = tuple(
        (int(x), int(x) - i) for i, x in enumerate(line.split(',')) if x != 'x'
    )
    nums, remainders = tuple(zip(*arr))
    return int(n), nums, remainders


def earliest_bus(n: int, nums: Numbers) -> int:
    min_wait, bus = min((x - (n % x), x) for x in nums)
    return min_wait * bus


def chinese_remainder_theorem(nums: Numbers, remainders: Numbers) -> int:
    product = prod(nums)
    total = 0
    for num, remainder in zip(nums, remainders):
        p = product // num
        total += remainder * pow(p, -1, num) * p
    return total % product


def solve() -> tuple[int, int]:
    n, nums, remainders = parse(read_puzzle())
    return earliest_bus(n, nums), chinese_remainder_theorem(nums, remainders)


if __name__ == '__main__':
    print(solve())
