# https://adventofcode.com/2019/day/4

import re

from utils_proxy import read_puzzle


def parse(s: str) -> tuple[int, ...]:
    return tuple(int(n) for n in s.split('-'))


def is_password(n: int, *, strict: bool = False) -> bool:
    s = str(n)
    runs = [run[0] for run in re.findall(r'((\d)\2+)', s)]
    if strict:
        runs = [run for run in runs if len(run) == 2]
    return bool(runs) and sorted(s) == list(s)


def count_in_range(from_: int, to: int, *, strict: bool = False) -> int:
    range_ = range(from_, to + 1)
    return sum(1 for n in range_ if is_password(n, strict=strict))


def solve() -> tuple[int, int]:
    from_, to = parse(read_puzzle())
    part1 = count_in_range(from_, to)
    part2 = count_in_range(from_, to, strict=True)
    return part1, part2


if __name__ == '__main__':
    print(solve())
