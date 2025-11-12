# https://adventofcode.com/2020/day/24

import re
from collections import Counter, defaultdict
from functools import cache, reduce
from typing import Literal, get_args

from helpers import read_puzzle

type Coord = tuple[int, int]
# can't use `type` for Dir because of get_args()
Dir = Literal['e', 'se', 'sw', 'w', 'nw', 'ne']

RE_DIR = r'(?:e|se|sw|w|nw|ne)'


def move(c: Coord, dir_: Dir) -> Coord:
    x, y = c
    match dir_:
        case 'e':
            return (x + 1, y)
        case 'se':
            return (x, y + 1)
        case 'sw':
            return (x - 1, y + 1)
        case 'w':
            return (x - 1, y)
        case 'nw':
            return (x, y - 1)
        case 'ne':
            return (x + 1, y - 1)


def parse(s: str) -> set[Coord]:
    guide = [re.findall(RE_DIR, line) for line in s.splitlines()]
    counter = Counter(reduce(move, dirs, (0, 0)) for dirs in guide)
    return {c for c, count in counter.items() if count % 2 == 1}


@cache
def around(c: Coord) -> tuple[Coord, ...]:
    return tuple(move(c, dir_) for dir_ in get_args(Dir))


def cycle(tiles: set[Coord]) -> set[Coord]:
    adj: defaultdict[Coord, int] = defaultdict(int)
    for c in tiles:
        for c2 in around(c):
            adj[c2] += 1
    next_tiles = {c for c in tiles if adj[c] in {1, 2}}
    for c, n in adj.items():
        if n == 2 and c not in tiles:
            next_tiles.add(c)
    return next_tiles


def solve() -> tuple[int, int]:
    tiles = orig_tiles = parse(read_puzzle())
    for _ in range(100):
        tiles = cycle(tiles)
    return len(orig_tiles), len(tiles)


if __name__ == '__main__':
    print(solve())
