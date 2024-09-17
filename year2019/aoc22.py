# https://adventofcode.com/2019/day/22


import re

from helpers import read_puzzle

REGEX = r'^(.+?)([-0-9]+)?$'


def shuffle(commands: list[str], size: int) -> tuple[int, int]:
    start, step = 0, 1
    for command in commands:
        m = re.match(REGEX, command)
        assert m is not None  # input is guaranteed to be correct
        match m.groups():
            case ('deal into new stack', None):
                start = (start - step) % size
                step = -step % size
            case ('cut ', n):
                start = (start + int(n) * step) % size
            case ('deal with increment ', n):
                step = (step * pow(int(n), -1, size)) % size
    return start, step


def view(start: int, step: int, size: int) -> tuple[int, ...]:
    return tuple((start + i * step) % size for i in range(size))


def part1(puzzle: list[str]) -> int:
    size = 10007
    start, step = shuffle(puzzle, size)
    return view(start, step, size).index(2019)


def part2(puzzle: list[str]) -> int:
    size, times = 119_315_717_514_047, 101_741_582_076_661
    start, step = shuffle(puzzle, size)
    step2 = pow(step, times, size)
    start2 = start * (step2 - 1) * pow(step - 1, -1, size) % size
    return (start2 + 2020 * step2) % size


def solve() -> tuple[int, int]:
    puzzle = read_puzzle().splitlines()
    return part1(puzzle), part2(puzzle)


if __name__ == '__main__':
    print(solve())
