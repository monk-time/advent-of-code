# https://adventofcode.com/2021/day/1
# tags: #sliding-window

from operator import lt

from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [int(line) for line in s.split()]


def count_increases(a: list[int], *, window: int) -> int:
    return sum(map(lt, a, a[window:], strict=False))


def solve() -> tuple[int, int]:
    a = parse(read_puzzle())
    return (count_increases(a, window=1), count_increases(a, window=3))


if __name__ == '__main__':
    print(solve())
