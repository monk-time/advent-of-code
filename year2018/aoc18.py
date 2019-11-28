from collections import Counter, defaultdict
from itertools import product
from typing import Dict, Tuple

from helpers import read_puzzle


def create_trans_table() -> Dict[str, str]:
    table = {}
    keys = (''.join(t) for t in product('.|#', repeat=9))
    for key in keys:
        adj, val = key[:4] + key[5:], key[4]
        c = Counter(adj)
        table[key] = (
            '|' if val == '.' and c['|'] >= 3 else
            '#' if val == '|' and c['#'] >= 3 else
            '.' if val == '#' and (c['#'] * c['|'] == 0) else
            val)
    return table


table = create_trans_table()


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
        trees, lumber = 0, 0
        adj = ((y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
               (y, x - 1), (y, x + 1),
               (y + 1, x - 1), (y + 1, x), (y + 1, x + 1))
        for y_, x_ in adj:
            val = self.m[y_, x_]
            if val == '|':
                trees += 1
            elif val == '#':
                lumber += 1
        return trees, lumber

    def tick(self):
        m = defaultdict(lambda: '.')
        for y, x in product(range(self.width), range(self.height)):
            sq = product(range(y - 1, y + 2), range(x - 1, x + 2))
            key = ''.join(self.m[t] for t in sq)
            m[(y, x)] = table[key]
        self.m = m


def count_after_n_ticks(m: Map, ticks: int) -> Tuple[int, int]:
    for _ in range(ticks):
        m.tick()
    c = Counter(m.m.values())
    return c['|'] * c['#']


def solve():
    m = Map(read_puzzle())
    return count_after_n_ticks(m, 10), count_after_n_ticks(m, 10 ** 3 - 10)


if __name__ == '__main__':
    print(solve())
