# https://adventofcode.com/2020/day/10

from collections import Counter, defaultdict
from itertools import pairwise

from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split()]


def difference(arr: list[int]) -> int:
    arr = sorted(arr)
    c = Counter(b - a for a, b in pairwise([0, *arr, arr[-1] + 3]))
    return c[1] * c[3]


def count_chains(arr: list[int]) -> int:
    arr = sorted(arr)
    max_value = arr[-1] + 3
    counts = defaultdict(int, {0: 1})
    for n in [*arr, max_value]:
        counts[n] = sum(counts[n - 1 - d] for d in range(3))
    return counts[max_value]


def solve() -> tuple[int, int]:
    arr = parse(read_puzzle())
    return difference(arr), count_chains(arr)


if __name__ == '__main__':
    print(solve())
