# https://adventofcode.com/2022/day/5
# tags:

from utils_proxy import read_puzzle

type InputType = list[int]


def parse(s: str) -> InputType:
    return [0 for _line in s.splitlines()]


def part1(_x: InputType) -> int:
    return 0


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    return part1(puzzle), 0


if __name__ == '__main__':
    print(solve())
