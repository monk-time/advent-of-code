# https://adventofcode.com/2018/day/10

import re
from collections import namedtuple

from helpers import read_puzzle

Point = namedtuple('Point', 'x y dx dy')
Points = list[Point]


def parse(s: str) -> Points:
    return [
        Point(*map(int, re.findall(r'-?\d+', line))) for line in s.splitlines()
    ]


def dimensions(points: Points) -> tuple[int, int, int, int]:
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    return w, h, min_x, min_y


def points_to_str(points: Points) -> str:
    w, h, min_x, min_y = dimensions(points)
    screen = ['.' * w] * h
    for p in points:
        x, y = p.x - min_x, p.y - min_y
        s = screen[y]
        screen[y] = s[:x] + '#' + s[x + 1 :]
    return '\n'.join(screen)


def move_all(points: Points) -> Points:
    return [Point(p.x + p.dx, p.y + p.dy, p.dx, p.dy) for p in points]


def move_while_shrinks(points: Points):
    dims, sec = dimensions(points), 0
    while True:
        dims_old, points_old = dims, points
        points = move_all(points)
        dims = dimensions(points)
        if dims_old[0] < dims[0] or dims_old[1] < dims[1]:
            break
        sec += 1
    return points_to_str(points_old), sec


def solve():
    return move_while_shrinks(parse(read_puzzle()))


if __name__ == '__main__':
    print(*solve())
