# https://adventofcode.com/2018/day/25

from itertools import combinations

from helpers import read_puzzle

Point = tuple[int, ...]


def parse(s: str):
    return [tuple(int(n) for n in line.split(',')) for line in s.splitlines()]


def dist(p1: Point, p2: Point) -> int:
    return sum(abs(x - y) for x, y in zip(p1, p2))


def count_constellations(points: list[Point]) -> int:
    cstls = {p: frozenset([p]) for p in points}
    for p1, p2 in combinations(points, 2):
        if dist(p1, p2) <= 3:
            new_cstl = frozenset(cstls[p1] | cstls[p2])
            for p in new_cstl:
                cstls[p] = new_cstl
    return len(set(cstls.values()))


def solve():
    return count_constellations(parse(read_puzzle()))


if __name__ == '__main__':
    print(solve())
