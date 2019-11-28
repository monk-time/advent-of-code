from collections import Counter, defaultdict
from itertools import product
from typing import Dict, Tuple

from helpers import read_puzzle

Table = Dict[Tuple[int, int], int]


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

    def summed_area_tables(self) -> Tuple[Table, Table]:
        tr: Table = defaultdict(int)  # n of trees from (0, 0) to (y, x)
        ly: Table = defaultdict(int)  # n of lumberyards from (0, 0) to (y, x)
        for y, x in product(range(self.height + 1), range(self.width + 1)):
            for t, ch in ((tr, '|'), (ly, '#')):
                n = 1 if self.m[(y, x)] == ch else 0
                t[(y, x)] = n + t[(y - 1, x)] + t[(y, x - 1)] - t[(y - 1, x - 1)]
        return tr, ly

    def tick(self):
        m = defaultdict(lambda: '.')
        tr, ly = self.summed_area_tables()
        for y, x in product(range(self.height), range(self.width)):
            c = {}
            for table, ch in ((tr, '|'), (ly, '#')):
                c[ch] = table[(y + 1, x + 1)] + table[(y - 2, x - 2)] - \
                        table[(y - 2, x + 1)] - table[(y + 1, x - 2)] - \
                        (1 if self.m[(y, x)] == ch else 0)
            t = (y, x)
            m[t] = (
                '|' if self.m[t] == '.' and c['|'] >= 3 else
                '#' if self.m[t] == '|' and c['#'] >= 3 else
                '.' if self.m[t] == '#' and c['#'] * c['|'] == 0 else
                self.m[t])
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
