# https://adventofcode.com/2020/day/15

from collections import defaultdict
from itertools import islice
from typing import TYPE_CHECKING

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator

PART_1 = 2020
PART_2 = 30000000


def parse(s: str) -> tuple[int, ...]:
    return tuple(int(x) for x in s.split(','))


def gen_memory_game(start_nums: tuple[int, ...]) -> Generator[int]:
    last_seen: defaultdict[int, int | None] = defaultdict(lambda: None)
    turn, n = 0, 0
    for turn, n in enumerate(start_nums, start=1):
        last_seen[n] = turn
        yield n
    while True:
        prev, last_seen[n] = last_seen[n], turn
        yield (n := 0 if prev is None else turn - prev)
        turn += 1


def get_nth_num(start_nums: tuple[int, ...], n: int) -> int:
    return next(islice(gen_memory_game(start_nums), n - 1, None))


def solve() -> tuple[int, int]:
    start_nums = parse(read_puzzle())
    return get_nth_num(start_nums, PART_1), get_nth_num(start_nums, PART_2)


if __name__ == '__main__':
    print(solve())
