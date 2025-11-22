# https://adventofcode.com/2020/day/9

from collections import Counter
from itertools import combinations

from utils_proxy import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split()]


def find_invalid(arr: list[int], preamble: int) -> int:
    sums = Counter(sum(c) for c in combinations(arr[:preamble], 2))
    for i in range(preamble, len(arr)):
        if (cur := arr[i]) not in sums:
            return cur
        drop = arr[i - preamble]
        for j in range(i - preamble + 1, i):
            sum_ = drop + arr[j]
            sums[sum_] -= 1
            if not sums[sum_]:
                del sums[sum_]
            sums[cur + arr[j]] += 1
    return 0


def find_contiguous_sum(arr: list[int], total: int):
    acc, i, j = arr[0], 0, 0
    while acc != total:
        while acc < total:
            j += 1
            acc += arr[j]
        while acc > total:
            acc -= arr[i]
            i += 1
    sum_range = arr[i : j + 1]
    return min(sum_range) + max(sum_range)


def solve() -> tuple[int, int]:
    arr = parse(read_puzzle())
    invalid = find_invalid(arr, 25)
    return invalid, find_contiguous_sum(arr, invalid)


if __name__ == '__main__':
    print(solve())
