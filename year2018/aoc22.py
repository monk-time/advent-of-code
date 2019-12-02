import re
from itertools import product
from typing import Dict, Tuple

from helpers import read_puzzle

Point = Tuple[int, int]
Map = Dict[Point, int]


def parse(s: str) -> Tuple[int, Point]:
    depth, x, y = map(int, re.findall(r'\d+', s))
    return depth, (y, x)


def gen_map(depth: int, target: Point) -> Map:
    y_t, x_t = target
    m: Map = {}
    for y, x in product(range(y_t + 1), range(x_t + 1)):
        geoindex = (0 if (y, x) == target else
                    x * 16807 if y == 0 else
                    y * 48271 if x == 0 else
                    m[(y - 1, x)] * m[(y, x - 1)])
        m[(y, x)] = (geoindex + depth) % 20183
    return m


def map_to_str(m: Map) -> str:
    y_t, x_t = list(m.keys())[-1]
    s = '\n'.join(''.join('.=|'[m[(y, x)] % 3] for x in range(x_t + 1))
                  for y in range(y_t + 1))
    s = 'M' + s[1:-1] + 'T'
    return s


def calc_risk(m: Map) -> int:
    return sum(n % 3 for n in m.values())


def solve():
    m = gen_map(*parse(read_puzzle()))
    return calc_risk(m)


if __name__ == '__main__':
    print(solve())
