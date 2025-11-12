# https://adventofcode.com/2021/day/11

from helpers import read_puzzle


def parse(s: str) -> list[int]:
    return [0 for _line in s.split()]


def solve() -> tuple[int, int]:
    _puzzle = parse(read_puzzle())
    return 0, 0


if __name__ == '__main__':
    print(solve())
