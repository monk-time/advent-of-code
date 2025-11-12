# https://adventofcode.com/2020/day/24

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import cache, reduce
from typing import Literal, Self, get_args

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


@cache
def around(c: Coord) -> tuple[Coord, ...]:
    return tuple(move(c, dir_) for dir_ in get_args(Dir))


@dataclass
class State:
    active: set[Coord] = field(default_factory=set)  # black tiles are active
    has_2: set[Coord] = field(default_factory=set)  # 2 active neighbors
    adj: defaultdict[Coord, int] = field(
        default_factory=lambda: defaultdict(int)
    )

    @classmethod
    def from_str(cls, s: str) -> Self:
        guide = [re.findall(RE_DIR, line) for line in s.splitlines()]
        counter = Counter(reduce(move, dirs, (0, 0)) for dirs in guide)
        black_tiles = {c for c, count in counter.items() if count % 2 == 1}
        state = cls()
        for c in black_tiles:
            state.toggle(c, delta=1)
        return state

    def toggle(self, c: Coord, *, delta: int) -> None:
        for c2 in around(c):
            self.adj[c2] += delta
            if self.adj[c2] == 2:
                self.has_2.add(c2)
            else:
                self.has_2.discard(c2)
        if delta == 1:
            self.active.add(c)
        else:
            self.active.remove(c)

    def cycle(self) -> None:
        disable = {
            c for c in self.active if self.adj[c] == 0 or self.adj[c] > 2
        }
        enable = self.has_2 - self.active
        for coords, delta in ((disable, -1), (enable, 1)):
            for c in coords:
                self.toggle(c, delta=delta)


def solve() -> tuple[int, int]:
    st = State.from_str(read_puzzle())
    part1 = len(st.active)
    for _ in range(100):
        st.cycle()
    part2 = len(st.active)
    return part1, part2


if __name__ == '__main__':
    print(solve())
