# https://adventofcode.com/2020/day/17

from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from itertools import product
from typing import Self

from utils_proxy import read_puzzle

type Coord = tuple[int, ...]


@cache
def around(c: Coord) -> tuple[Coord, ...]:
    return tuple(
        tuple(map(sum, zip(c, delta)))
        for delta in product(range(-1, 2), repeat=len(c))
        if not all(i == 0 for i in delta)
    )


@dataclass
class State:
    dim: int
    active: set[Coord] = field(default_factory=set[Coord])
    has_2: set[Coord] = field(default_factory=set[Coord])  # 2 active neighbors
    has_3: set[Coord] = field(default_factory=set[Coord])  # 3 active neighbors
    neighbor_count: defaultdict[Coord, int] = field(
        default_factory=lambda: defaultdict(int)
    )

    @classmethod
    def from_str(cls, s: str, *, dim: int) -> Self:
        lines = s.splitlines()
        state = cls(dim=dim)
        for x in range(len(lines[0])):
            for y in range(len(lines)):
                if lines[y][x] == '#':
                    c = (x, y, *(0,) * (dim - 2))
                    state.toggle(c, delta=1)
        return state

    def toggle(self, c: Coord, *, delta: int) -> None:
        for c2 in around(c):
            self.neighbor_count[c2] += delta
            if self.neighbor_count[c2] == 2:
                self.has_2.add(c2)
            else:
                self.has_2.discard(c2)
            if self.neighbor_count[c2] == 3:
                self.has_3.add(c2)
            else:
                self.has_3.discard(c2)
        if delta == 1:
            self.active.add(c)
        else:
            self.active.remove(c)

    def cycle(self) -> None:
        disable = self.active - self.has_2 - self.has_3
        enable = self.has_3 - self.active
        for coords, delta in ((disable, -1), (enable, 1)):
            for c in coords:
                self.toggle(c, delta=delta)


def solve() -> tuple[int, int]:
    st_1 = State.from_str(read_puzzle(), dim=3)
    for _ in range(6):
        st_1.cycle()
    st_2 = State.from_str(read_puzzle(), dim=4)
    for _ in range(6):
        st_2.cycle()
    return len(st_1.active), len(st_2.active)


if __name__ == '__main__':
    print(solve())
