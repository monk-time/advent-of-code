# https://adventofcode.com/2019/day/22


import re
from math import floor, log2

from helpers import read_puzzle

REGEX = r'^(.+?)([-0-9]+)?$'


def shuffle(commands: list[str], size: int) -> tuple[int, int]:
    start, step = 0, 1
    for command in commands:
        m = re.match(REGEX, command)
        if not m:
            msg = f'Unexpected command: {m}'
            raise ValueError(msg)
        match m.groups():
            case ('deal into new stack', None):
                start = (start - step) % size
                step = -step % size
            case ('cut ', n):
                i = int(n) % size
                start = (start + i * step) % size
            case ('deal with increment ', n):
                i = int(n)
                step = (step * bezout(i, size)) % size
    return start, step


def bezout(a: int, b: int) -> int:
    """Solve Bezout equation `ax + by = 1`. Returns only x."""
    x, x2, b0 = 1, 0, b
    while b:
        q = a // b
        a, b = b, a % b
        x, x2 = x2, x - x2 * q
    return x % b0


def view(start: int, step: int, size: int) -> tuple[int, ...]:
    return tuple((start + i * step) % size for i in range(size))


def part1(puzzle: list[str]) -> int:
    size = 10007
    start, step = shuffle(puzzle, size)
    return view(start, step, size).index(2019)


type Shuffle = tuple[int, int]


def part2(puzzle: list[str]) -> int:
    def add(sh1: Shuffle, sh2: Shuffle, size: int) -> Shuffle:
        start1, step1, start2, step2 = *sh1, *sh2
        return ((start1 + start2 * step1) % size, (step1 * step2) % size)

    size = 119_315_717_514_047
    total_times = 101_741_582_076_661
    key = shuffle(puzzle, size)
    cache = {1: key}
    for i in range(1, floor(log2(total_times)) + 1):
        key = add(key, key, size)
        cache[2**i] = key
    key = (0, 1)
    while total_times > 0:
        i = 2 ** floor(log2(total_times))
        key = add(key, cache[i], size)
        total_times -= i
    return (key[0] + 2020 * key[1]) % size


def solve() -> tuple[int, int]:
    puzzle = read_puzzle().splitlines()
    return part1(puzzle), part2(puzzle)


if __name__ == '__main__':
    print(solve())
