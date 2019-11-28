from collections import Counter, defaultdict
from itertools import product
from typing import Tuple

from helpers import read_puzzle


class Map:
    def __init__(self, s: str):
        self.m = defaultdict(lambda: '.')
        lines = s.splitlines()
        self.height = len(lines)
        self.width = len(lines[0])
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                self.m[(i, j)] = ch

    def __str__(self):
        """Get a text representation of the map."""
        return '\n'.join([''.join(self.m[(i, j)] for j in range(self.width))
                          for i in range(self.height)])

    def count_adj(self, y, x):
        return Counter(
            (self.m[y - 1, x - 1], self.m[y - 1, x], self.m[y - 1, x + 1],
             self.m[y, x - 1], self.m[y, x + 1],
             self.m[y + 1, x - 1], self.m[y + 1, x], self.m[y + 1, x + 1]))

    def tick(self):
        m = defaultdict(lambda: '.')
        for t in product(range(self.width), range(self.height)):
            n = self.count_adj(*t)
            m[t] = (
                '|' if self.m[t] == '.' and n['|'] >= 3 else
                '#' if self.m[t] == '|' and n['#'] >= 3 else
                '.' if self.m[t] == '#' and (n['#'] == 0 or n['|'] == 0) else
                self.m[t])
        self.m = m


def count_after_n_ticks(m: Map, ticks: int) -> Tuple[int, int]:
    for _ in range(ticks):
        m.tick()
    c = Counter(m.m.values())
    return c['|'] * c['#']


def solve():
    m = Map(read_puzzle())
    return count_after_n_ticks(m, 10),


if __name__ == '__main__':
    print(solve())
