# https://adventofcode.com/2019/day/10

from itertools import product
from math import gcd
from typing import TYPE_CHECKING

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

Map = list[list[str]]
Coord = tuple[int, int]


def parse(s: str) -> Map:
    return [list(line) for line in s.split()]


def get_shifts(x: int, y: int, m: Map) -> Iterable[tuple[int, int]]:
    height, width = len(m), len(m[0])
    for dx, dy in product(
        range(-width + 1, width), range(-height + 1, height)
    ):
        if (
            (dx, dy) != 0
            and gcd(dx, dy) == 1
            and 0 <= x + dx < width
            and 0 <= y + dy < height
        ):
            yield dx, dy


def count_visible_from(x: int, y: int, m: Map) -> int:
    height, width = len(m), len(m[0])
    count = 0
    for dx, dy in get_shifts(x, y, m):
        x2, y2 = x, y
        while 0 <= x2 + dx < width and 0 <= y2 + dy < height:
            x2 += dx
            y2 += dy
            if m[y2][x2] == '#':
                count += 1
                break
    return count


def find_best_location(m: Map) -> tuple[int, int, int]:
    height, width = len(m), len(m[0])
    max_count, max_x, max_y = 0, 0, 0
    for x, y in product(range(width), range(height)):
        if m[y][x] != '#':
            continue
        count = count_visible_from(x, y, m)
        if count > max_count:
            max_count, max_x, max_y = count, x, y
    return max_count, max_x, max_y


def sign(x: int) -> int:
    return (x > 0) - (x < 0)


angles: list[tuple[int, int]] = [
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
]


def radial_sort(t: tuple[int, int]) -> tuple[int, float]:
    dx, dy = t
    key_angle = angles.index((sign(dx), sign(dy)))
    key_value = 0 if key_angle % 2 == 0 else dy / dx
    return key_angle, key_value


def get_radial_shifts(x: int, y: int, m: Map) -> Iterable[Coord]:
    yield from sorted(get_shifts(x, y, m), key=radial_sort)


def vaporize_from(x: int, y: int, m: Map) -> Iterable[Coord]:
    height, width = len(m), len(m[0])
    count = 1
    m = [line[:] for line in m]
    while count:
        count = 0
        for dx, dy in get_radial_shifts(x, y, m):
            x2, y2 = x, y
            while 0 <= x2 + dx < width and 0 <= y2 + dy < height:
                x2 += dx
                y2 += dy
                if m[y2][x2] == '#':
                    count += 1
                    m[y2][x2] = '.'
                    yield x2, y2
                    break


def solve() -> Coord:
    puzzle = parse(read_puzzle())
    max_count, x, y = find_best_location(puzzle)
    vaporized = list(vaporize_from(x, y, puzzle))
    x2, y2 = vaporized[199]
    return max_count, x2 * 100 + y2


if __name__ == '__main__':
    print(solve())
