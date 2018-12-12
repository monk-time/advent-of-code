import re
from dataclasses import dataclass
from typing import Iterable, List, Tuple

from helpers import read_puzzle


@dataclass
class Point:
    pos: Tuple[int, int]
    delta: Tuple[int, int]


Points = List[Point]


def parse(s: str) -> Iterable[Point]:
    for line in s.splitlines():
        x, y, dx, dy = map(int, re.findall(r'-?\d+', line))
        yield Point((x, y), (dx, dy))


def move_all(points: Points) -> Points:
    return [Point((p.pos[0] + p.delta[0], p.pos[1] + p.delta[1]), p.delta)
            for p in points]


def dimensions(points: Points) -> Tuple[int, int, int, int]:
    min_x = min(p.pos[0] for p in points)
    max_x = max(p.pos[0] for p in points)
    min_y = min(p.pos[1] for p in points)
    max_y = max(p.pos[1] for p in points)
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    return w, h, min_x, min_y


def solve(points: Points):
    dims, sec = dimensions(points), 0
    while True:
        dims_old, points_old = dims, points
        points = move_all(points)
        dims = dimensions(points)
        if dims_old[0] < dims[0] or dims_old[1] < dims[1]:
            break
        sec += 1
    points = points_old
    w, h, min_x, min_y = dims_old
    screen = ['.' * w] * h
    for p in points:
        x, y = p.pos[0] - min_x, p.pos[1] - min_y
        s = screen[y]
        screen[y] = s[:x] + '#' + s[x + 1:]
    return '\n'.join(screen), sec


if __name__ == '__main__':
    points_ = list(parse(read_puzzle()))
    print(*solve(points_))
