# https://adventofcode.com/2020/day/1

from itertools import combinations
from math import prod

from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split()]


def split_into_elements(arr: list[int], k: int, total: int = 2020) -> int:
    return prod(next(c for c in combinations(arr, k) if sum(c) == total))


def solve() -> tuple[int, int]:
    arr = parse(read_puzzle())
    return split_into_elements(arr, 2), split_into_elements(arr, 3)


if __name__ == '__main__':
    print(solve())
