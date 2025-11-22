# https://adventofcode.com/2021/day/5
# tags: #grid #angle

import re
from collections import Counter
from functools import partial
from itertools import batched, chain, starmap
from typing import TYPE_CHECKING, cast

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

type Coord = tuple[int, int]
type Pipe = tuple[Coord, Coord]


def parse(s: str) -> Iterable[Pipe]:
    for line in s.split('\n'):
        a, b = batched(map(int, re.findall(r'\d+', line)), 2, strict=True)
        yield cast('Coord', a), cast('Coord', b)


def line(a: Coord, b: Coord, *, with_diag: bool = False) -> Iterable[Coord]:
    dx, dy = b[0] - a[0], b[1] - a[1]
    x_sign = 1 if dx > 0 else -1 if dx < 0 else 0
    y_sign = 1 if dy > 0 else -1 if dy < 0 else 0
    delta = max(abs(dx), abs(dy))
    if dx == 0 or dy == 0 or (with_diag and abs(dx) == abs(dy)):
        yield from (
            (a[0] + i * x_sign, a[1] + i * y_sign) for i in range(delta + 1)
        )


def count_overlaps(pipes: Iterable[Pipe], *, with_diag: bool = False) -> int:
    line_func = line if not with_diag else partial(line, with_diag=True)
    lines = starmap(line_func, pipes)
    counter = Counter(chain.from_iterable(lines))
    return sum(1 for n in counter.values() if n >= 2)


def solve() -> tuple[int, int]:
    pipes = list(parse(read_puzzle()))
    return count_overlaps(pipes), count_overlaps(pipes, with_diag=True)


if __name__ == '__main__':
    print(solve())
