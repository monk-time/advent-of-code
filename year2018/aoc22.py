import re
from itertools import product
from typing import Dict, Iterable, Tuple

import networkx as nx

from helpers import read_puzzle

Point = Tuple[int, int]


class Map:
    def __init__(self, s: str, extra: int = 0):
        depth, x, y = map(int, re.findall(r'\d+', s))
        self.depth: int = depth
        self.target: Point = (y, x)
        self.erosion: Dict[Point, int] = {}
        self.cave: Dict[Point, str] = {}
        self.generate(extra)
        self.last_gen: Point = (y + extra, x + extra)

    def generate(self, extra: int = 0):
        y_t, x_t = self.target
        for y, x in product(range(y_t + 1 + extra), range(x_t + 1 + extra)):
            geoindex = (0 if (y, x) == self.target else
                        x * 16807 if y == 0 else
                        y * 48271 if x == 0 else
                        self.erosion[(y - 1, x)] * self.erosion[(y, x - 1)])
            self.erosion[(y, x)] = (geoindex + self.depth) % 20183
            self.cave[(y, x)] = '.=|'[self.erosion[(y, x)] % 3]
        self.cave[(0, 0)] = 'M'
        self.cave[self.target] = 'T'

    def __str__(self):
        y_max, x_max = self.last_gen
        return '\n'.join(''.join(self.cave[(y, x)] for x in range(x_max + 1))
                         for y in range(y_max + 1))

    def adj(self, y: int, x: int) -> Iterable[Point]:
        y_max, x_max = self.last_gen
        return ((y2, x2) for y2, x2 in ((y - 1, x), (y, x - 1),
                                        (y, x + 1), (y + 1, x))
                if 0 <= x2 <= x_max and 0 <= y2 <= y_max)


risk = {'M': 0, 'T': 0, '.': 0, '=': 1, '|': 2}


def calc_risk(m: Map) -> int:
    y_t, x_t = m.target
    return sum(risk[m.cave[(y, x)]]
               for y in range(y_t + 1) for x in range(x_t + 1))


# t = torch, c = climbing gear, n = none
tools = {'M': 't', 'T': 'ct', '.': 'ct', '=': 'cn', '|': 'tn'}


def shortest_path(m: Map):
    edges = [((p1, t1), (p2, t2), {'weight': 1 if t1 == t2 else 8})
             for p1 in m.cave.keys()
             for p2 in m.adj(*p1)
             for t1 in tools[m.cave[p1]]
             for t2 in tools[m.cave[p2]] if t2 in tools[m.cave[p1]]]
    # Ensure that the torch is equipped after reaching the target
    edges.append(((m.target, 'c'), (m.target, 't'), {'weight': 7}))

    g = nx.Graph(edges)
    return nx.dijkstra_path_length(g, ((0, 0), 't'), (m.target, 't'))


def solve():
    m = Map(read_puzzle(), extra=20)
    return calc_risk(m), shortest_path(m)


if __name__ == '__main__':
    print(solve())
