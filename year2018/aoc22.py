import re
from itertools import product
from typing import Dict, Tuple

from helpers import read_puzzle

Point = Tuple[int, int]


class Map:
    def __init__(self, s: str):
        depth, x, y = map(int, re.findall(r'\d+', s))
        self.depth: int = depth
        self.target: Point = (y, x)
        self.erosion: Dict[Point, int] = {}
        self.cave: Dict[Point, str] = {}
        self.gen_to_target()
        self.last_gen: Point = self.target

    def gen_region(self, y: int, x: int):
        geoindex = (0 if (y, x) == self.target else
                    x * 16807 if y == 0 else
                    y * 48271 if x == 0 else
                    self.erosion[(y - 1, x)] * self.erosion[(y, x - 1)])
        self.erosion[(y, x)] = (geoindex + self.depth) % 20183
        self.cave[(y, x)] = '.=|'[self.erosion[(y, x)] % 3]

    def gen_to_target(self):
        y_t, x_t = self.target
        for y, x in product(range(y_t + 1), range(x_t + 1)):
            self.gen_region(y, x)
        self.cave[(0, 0)] = 'M'
        self.cave[self.target] = 'T'

    def gen_deeper(self):
        y_last, x_last = self.last_gen
        for y in range(y_last + 1):
            self.gen_region(y, x_last + 1)
        for x in range(x_last + 1):
            self.gen_region(y_last + 1, x)
        self.gen_region(y_last + 1, x_last + 1)
        self.last_gen = y_last + 1, x_last + 1

    def __str__(self):
        y_t, x_t = self.last_gen
        return '\n'.join(''.join(self.cave[(y, x)] for x in range(x_t + 1))
                         for y in range(y_t + 1))


risk = {'M': 0, 'T': 0, '.': 0, '=': 1, '|': 2}


def calc_risk(m: Map) -> int:
    y_t, x_t = m.target
    return sum(risk[m.cave[(y, x)]]
               for y in range(y_t + 1) for x in range(x_t + 1))


def fastest_route(m: Map) -> int:
    pass


def solve():
    m = Map(read_puzzle())
    return calc_risk(m)


if __name__ == '__main__':
    print(solve())
