# https://adventofcode.com/2018/day/22

import re
from itertools import product
from typing import TYPE_CHECKING

import networkx as nx

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

Point = tuple[int, int]


class Map:
    def __init__(self, s: str, extra: int = 0):
        depth, x, y = map(int, re.findall(r'\d+', s))
        self.depth: int = depth
        self.target: Point = (y, x)
        self.erosion: dict[Point, int] = {}
        self.cave: dict[Point, str] = {}
        self.generate(extra)
        self.corner: Point = (y + extra, x + extra)

    def generate(self, extra: int = 0):
        y_t, x_t = self.target
        for y, x in product(range(y_t + extra + 1), range(x_t + extra + 1)):
            geoindex = (
                0
                if (y, x) == self.target
                else x * 16807
                if y == 0
                else y * 48271
                if x == 0
                else self.erosion[y - 1, x] * self.erosion[y, x - 1]
            )
            self.erosion[y, x] = (geoindex + self.depth) % 20183
            self.cave[y, x] = '.=|'[self.erosion[y, x] % 3]

    def __str__(self):
        y_max, x_max = self.corner
        return '\n'.join(
            ''.join(
                'M'
                if (y, x) == (0, 0)
                else 'T'
                if (y, x) == self.target
                else self.cave[y, x]
                for x in range(x_max + 1)
            )
            for y in range(y_max + 1)
        )

    def adj(self, y: int, x: int) -> Iterable[Point]:
        y_max, x_max = self.corner
        return (
            (y2, x2)
            for y2, x2 in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x))
            if 0 <= x2 <= x_max and 0 <= y2 <= y_max
        )


def calc_risk(m: Map) -> int:
    y_t, x_t = m.target
    return sum(
        '.=|'.index(m.cave[y, x])
        for y in range(y_t + 1)
        for x in range(x_t + 1)
    )


# t = torch, c = climbing gear, n = none
tool_map = {'.': 'ct', '=': 'cn', '|': 'tn'}


def shortest_path(m: Map):
    g = nx.Graph()
    for p1 in m.cave:
        tools = tool_map[m.cave[p1]]
        g.add_edge((p1, tools[0]), (p1, tools[1]), weight=7)
        for p2 in m.adj(*p1):
            tools2 = tool_map[m.cave[p2]]
            for item in set(tools) & set(tools2):
                g.add_edge((p1, item), (p2, item), weight=1)

    return nx.dijkstra_path_length(g, ((0, 0), 't'), (m.target, 't'))


def solve():
    m = Map(read_puzzle(), extra=20)
    return calc_risk(m), shortest_path(m)


if __name__ == '__main__':
    print(solve())
