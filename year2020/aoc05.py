# https://adventofcode.com/2020/day/5


from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator


def parse(s: str) -> Generator[tuple[int, int]]:
    table = str.maketrans('FBLR', '0101')
    for line in s.split():
        binary = line.translate(table)
        yield int(binary[:7], 2), int(binary[7:], 2)


def solve() -> tuple[int, int]:
    seat_ids = {a * 8 + b for (a, b) in parse(read_puzzle())}
    return (
        max(seat_ids),
        sum(range(min(seat_ids), max(seat_ids) + 1)) - sum(seat_ids),
    )


if __name__ == '__main__':
    print(solve())
