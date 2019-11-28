from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Dict, Tuple

from helpers import read_puzzle


@dataclass(frozen=True)
class Map:
    m: Dict[Tuple[int, int], str]
    height: int
    width: int

    @classmethod
    def fromstring(cls, s: str):
        m = {}
        lines = s.splitlines()
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                m[(i, j)] = ch
        return Map(m, height=len(lines), width=len(lines[0]))

    def __str__(self):
        """Get a text representation of the map."""
        return '\n'.join([''.join(self.m[(i, j)] for j in range(self.width))
                          for i in range(self.height)])

    def __hash__(self):
        return hash(str(self))

    def count_adj(self, y, x):
        adj = ((y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
               (y, x - 1), (y, x + 1),
               (y + 1, x - 1), (y + 1, x), (y + 1, x + 1))
        return Counter(self.m.get(t, '.') for t in adj)

    def resource_value(self) -> Tuple[int, int]:
        c = Counter(self.m.values())
        return c['|'] * c['#']


def update(map_: Map) -> Map:
    m = defaultdict(lambda: '.')
    for t in product(range(map_.width), range(map_.height)):
        n = map_.count_adj(*t)
        val = map_.m.get(t, '.')
        m[t] = (
            '|' if val == '.' and n['|'] >= 3 else
            '#' if val == '|' and n['#'] >= 3 else
            '.' if val == '#' and n['#'] * n['|'] == 0 else
            val)
    return Map(m, map_.height, map_.width)


def count_after_n_ticks(map_: Map, ticks: int) -> Tuple[int, int]:
    tick, cache = 0, {}
    while map_ not in cache:
        tick += 1
        if tick > ticks:
            break
        cache[map_] = update(map_)
        map_ = cache[map_]
    else:  # no break, i.e. found a loop
        maps = list(cache.keys())
        loop = maps[maps.index(map_):]
        map_ = loop[(ticks - tick) % len(loop)]
    return map_.resource_value()


def solve():
    m = Map.fromstring(read_puzzle())
    return count_after_n_ticks(m, 10), count_after_n_ticks(m, 10 ** 9)


if __name__ == '__main__':
    print(solve())
