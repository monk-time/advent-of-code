from itertools import product
from math import gcd

from helpers import read_puzzle

Map = list[list[str]]


def parse(s: str) -> Map:
    return [list(line) for line in s.split()]


def count_visible_from(x: int, y: int, m: Map) -> int:
    height, width = len(m), len(m[0])
    count = 0
    for dx, dy in product(range(-width + 1, width), range(-height + 1, height)):
        if (dx, dy) == 0 or gcd(dx, dy) != 1:
            continue
        x2, y2 = x, y
        while 0 <= x2 + dx < width and 0 <= y2 + dy < height:
            x2 += dx
            y2 += dy
            if m[y2][x2] == '#':
                count += 1
                break
    return count


def find_best_location(m: Map) -> tuple[int, tuple[int, int]]:
    height, width = len(m), len(m[0])
    max_count, max_x, max_y = 0, 0, 0
    for x, y in product(range(0, width), range(0, height)):
        if m[y][x] != '#':
            continue
        count = count_visible_from(x, y, m)
        if count > max_count:
            max_count, max_x, max_y = count, x, y
    return max_count, (max_x, max_y)


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    max_count, *_ = find_best_location(puzzle)
    return max_count, 0


if __name__ == '__main__':
    print(solve())
