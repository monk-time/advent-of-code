# https://adventofcode.com/2021/day/17
# tags: #grid #angle

import re
from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator

type Coord = tuple[int, int]
type Area = tuple[Coord, Coord]


def parse(s: str) -> tuple[Coord, Coord]:
    x1, x2, y1, y2 = map(int, re.findall(r'-?\d+', s))
    return (x1, y1), (x2, y2)


def check_velocity(area: Area, v_x: int, v_y: int) -> int | None:
    x, y = 0, 0
    max_y = 0
    (x1, y1), (x2, y2) = area
    while True:
        x += v_x
        y += v_y
        max_y = max(max_y, y)
        v_x = max(v_x - 1, 0)
        v_y -= 1
        if x1 <= x <= x2 and y1 <= y <= y2:
            return max_y
        if y < y1 or x > x2:
            return None


def gen_max_heights(area: Area) -> Generator[int]:
    (_, y1), (x2, _) = area
    for v_x in range(1, x2 + 1):
        for v_y in range(y1, -y1 + 1):
            if (max_y := check_velocity(area, v_x, v_y)) is None:
                continue
            yield max_y


def solve() -> tuple[int, int]:
    c1, c2 = parse(read_puzzle())
    max_heights = list(gen_max_heights((c1, c2)))
    return max(max_heights), len(max_heights)


if __name__ == '__main__':
    print(solve())
