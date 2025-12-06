# https://adventofcode.com/2021/day/19
# tags: #grid #multidimensional-grid

import re
from collections import deque
from functools import cache
from itertools import batched, combinations, starmap
from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

type Coord = tuple[int, int, int]
type Coords = tuple[Coord, ...]
type Scanners = tuple[Coords, ...]
type DiffScanner = set[Coord]

CUTOFF = 12


def parse(s: str) -> Scanners:
    def parse_group(group: str) -> Generator[Coord]:
        nums = re.findall(r'-?[0-9]+', group)[1:]
        for x, y, z in batched(nums, n=3, strict=True):
            yield (int(x), int(y), int(z))

    return tuple(tuple(parse_group(group)) for group in s.split('\n\n'))


def rotate(c: Coord) -> Generator[Coord]:
    x, y, z = c
    faces = [c, (-x, y, -z), (y, z, x), (-y, z, -x), (z, x, y), (-z, x, -y)]
    for x2, y2, z2 in faces:
        for _ in range(4):
            yield (x2, y2, z2)
            y2, z2 = z2, -y2  # noqa: PLW2901


def rotate_all(scanner: Coords) -> Scanners:
    return tuple(zip(*map(rotate, scanner)))


def sub(a: Coord, b: Coord) -> Coord:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a: Coord, b: Coord) -> Coord:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def dist(a: Coord, b: Coord) -> int:
    return sum(abs(a[i] - b[i]) for i in range(3))


@cache
def get_diffs(scanner: Coords) -> dict[Coord, Coord]:
    # Assuming all beacons seen by a scanner have unique dists from each other
    return {sub(a, b): a for a, b in combinations(scanner, 2)}


def locate(scanners: Scanners) -> tuple[Scanners, Coords]:
    def intersect(sc: Coords, i: int) -> tuple[list[tuple[Coord, Coord]], int]:
        max_matches, max_dr_i = [], 0
        diffs_sc = get_diffs(sc)
        for dr_i, r in enumerate(rotations[i]):
            diffs_r = get_diffs(r)
            matches = [
                (diffs_sc[d], diffs_r[d]) for d in diffs_sc if d in diffs_r
            ]
            if len(matches) > len(max_matches):
                max_matches, max_dr_i = matches, dr_i
        return max_matches, max_dr_i

    rotations: list[Scanners] = [rotate_all(sc) for sc in scanners]
    adjustment_map: dict[int, Coords] = {0: scanners[0]}
    queue = deque[int](range(1, len(scanners)))
    positions = [(0, 0, 0)] * len(scanners)
    while queue:
        i = queue.popleft()
        for sc in adjustment_map.values():
            matches, dr_i = intersect(sc, i)
            if len(matches) < CUTOFF:
                continue
            positions[i] = pos = sub(*matches[0])
            adjustment_map[i] = tuple(add(c, pos) for c in rotations[i][dr_i])
            break
        else:  # nobreak
            queue.append(i)
    adjusted = tuple(v for _, v in sorted(adjustment_map.items()))
    return adjusted, tuple(positions)


def count_beacons(scanners: Scanners):
    return len({c for sc in scanners for c in sc})


def max_manhattan_dist(coords: Iterable[Coord]) -> int:
    return max(starmap(dist, combinations(coords, 2)))


def solve() -> tuple[int, int]:
    scanners = parse(read_puzzle())
    adjusted, positions = locate(scanners)
    return count_beacons(adjusted), max_manhattan_dist(positions)


if __name__ == '__main__':
    print(solve())
