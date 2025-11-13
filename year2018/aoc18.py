# https://adventofcode.com/2018/day/18

from collections import Counter
from dataclasses import dataclass
from itertools import product

from helpers import read_puzzle


@dataclass(frozen=True)
class Map:
    m: list[list[str]]
    height: int
    width: int

    @classmethod
    def fromstring(cls, s: str):
        lines = [list(line) for line in s.splitlines()]
        return Map(m=lines, height=len(lines), width=len(lines[0]))

    def __str__(self):
        """Get a text representation of the map."""
        return '\n'.join(''.join(row) for row in self.m)

    def __hash__(self):
        return hash(str(self))

    def count_adj(self, y: int, x: int) -> tuple[int, int]:
        adj = (
            (y - 1, x - 1),
            (y - 1, x),
            (y - 1, x + 1),
            (y, x - 1),
            (y, x + 1),
            (y + 1, x - 1),
            (y + 1, x),
            (y + 1, x + 1),
        )
        trees, lumber = 0, 0
        for y0, x0 in adj:
            if not (0 <= x0 < self.width and 0 <= y0 < self.height):
                continue
            val = self.m[y0][x0]
            if val == '|':
                trees += 1
            elif val == '#':
                lumber += 1
        return trees, lumber

    def resource_value(self) -> int:
        counter = Counter(str(self))
        return counter['|'] * counter['#']


def update(map_: Map) -> Map:
    m = [['.'] * map_.width for _ in range(map_.height)]
    for y, x in product(range(map_.width), range(map_.height)):
        trees, lumber = map_.count_adj(y, x)
        val = map_.m[y][x]
        m[y][x] = (
            '|'
            if val == '.' and trees >= 3
            else '#'
            if val == '|' and lumber >= 3
            else '.'
            if val == '#' and lumber * trees == 0
            else val
        )
    return Map(m, map_.height, map_.width)


def count_after_n_ticks(map_: Map, ticks: int) -> int:
    tick = 0
    cache: dict[Map, Map] = {}
    while map_ not in cache:
        tick += 1
        if tick > ticks:
            break
        cache[map_] = update(map_)
        map_ = cache[map_]
    else:  # no break, i.e. found a loop
        maps = list(cache.keys())
        loop = maps[maps.index(map_) :]
        map_ = loop[(ticks - tick) % len(loop)]
    return map_.resource_value()


def solve():
    m = Map.fromstring(read_puzzle())
    return count_after_n_ticks(m, 10), count_after_n_ticks(m, 10**9)


if __name__ == '__main__':
    print(solve())
