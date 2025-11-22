# https://adventofcode.com/2018/day/3

import re
from collections import Counter
from itertools import product
from typing import TYPE_CHECKING, NamedTuple

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable


class Claim(NamedTuple):
    id: int
    left: int
    top: int
    width: int
    height: int


def parse(claim: str) -> Claim:
    return Claim(*map(int, re.findall(r'\d+', claim)))


def parse_puzzle() -> list[Claim]:
    return [parse(line) for line in read_puzzle().splitlines()]


def squares(a: Claim) -> Iterable[tuple[int, int]]:
    return product(
        range(a.left, a.left + a.width), range(a.top, a.top + a.height)
    )


def overlap_and_count(claims: list[Claim]):
    layers = Counter(sq for c in claims for sq in squares(c))
    inches = sum(1 for v in layers.values() if v > 1)
    unused_id = next(
        c.id for c in claims if all(layers[sq] == 1 for sq in squares(c))
    )
    return inches, unused_id


def solve():
    return overlap_and_count(parse_puzzle())


if __name__ == '__main__':
    print(solve())
