# https://adventofcode.com/2019/day/22


import re

from helpers import read_puzzle

REGEX = r'^(.+?)([-0-9]+)?$'
SIZE_PART1 = 10007
SIZE_PART2 = 119315717514047


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
    """Solve Bezout equation `ax + by = 1` (ignore y)."""
    x, x2, b0 = 1, 0, b
    while b:
        q = a // b
        a, b = b, a % b
        x, x2 = x2, x - x2 * q
    return x % b0


def increment(step: int, size: int) -> list[int]:
    result = [0] * size
    cursor = 0
    for i in range(size):
        result[cursor] = i
        cursor = (cursor + step) % size
    return result


def view(size: int, start: int, step: int) -> tuple[int, ...]:
    return tuple((start + i * step) % size for i in range(size))


def solve() -> tuple[int, int]:
    puzzle = read_puzzle().splitlines()
    start, step = shuffle(puzzle, SIZE_PART1)
    part1 = view(SIZE_PART1, start, step).index(2019)
    return part1, 0


if __name__ == '__main__':
    print(solve())
