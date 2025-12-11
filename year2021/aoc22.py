# https://adventofcode.com/2021/day/22
# tags: #grid #multidimensional-grid #instructions #region-overlap

import re
from dataclasses import dataclass
from itertools import batched, product
from typing import TYPE_CHECKING, Literal

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator

type Action = Literal['on', 'off']
type Steps = tuple[tuple[Action, Region], ...]
type Coord = tuple[int, int, int]


@dataclass(frozen=True)
class Region:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def __contains__(self, c: Coord) -> bool:
        x, y, z = c
        return (
            self.x1 <= x <= self.x2
            and self.y1 <= y <= self.y2
            and self.z1 <= z <= self.z2
        )

    def overlaps(self, r: Region) -> bool:
        return (
            (self.x1 <= r.x2 and self.x2 >= r.x1)
            and (self.y1 <= r.y2 and self.y2 >= r.y1)
            and (self.z1 <= r.z2 and self.z2 >= r.z1)
        )

    def count_points(self) -> int:
        return (
            (self.x2 - self.x1 + 1)
            * (self.y2 - self.y1 + 1)
            * (self.z2 - self.z1 + 1)
        )


INIT_AREA = Region(-50, 50, -50, 50, -50, 50)


def parse(s: str) -> Steps:
    return tuple(
        (
            'off' if 'off' in line else 'on',
            Region(*map(int, re.findall(r'-?\d+', line))),
        )
        for line in s.splitlines()
    )


def add_extra_points(a: int, b: int, c: int, d: int) -> list[int]:
    a, b, c, d = sorted((a, b, c, d))
    return [a, b - 1, b, c, c + 1, d]


def sub(r1: Region, r2: Region) -> Generator[Region]:
    xs = add_extra_points(r1.x1, r1.x2, r2.x1, r2.x2)
    ys = add_extra_points(r1.y1, r1.y2, r2.y1, r2.y2)
    zs = add_extra_points(r1.z1, r1.z2, r2.z1, r2.z2)
    parts = product(*(batched(arr, 2, strict=True) for arr in (xs, ys, zs)))
    for (x1, x2), (y1, y2), (z1, z2) in parts:
        if x1 <= x2 and y1 <= y2 and z1 <= z2:
            c = (x1, y1, z1)
            if c in r1 and c not in r2:
                yield Region(x1, x2, y1, y2, z1, z2)


def reboot(steps: Steps, *, init_only: bool = False) -> int:
    regions = list[Region]()  # store only non-overlapping regions
    for action, region in steps:
        if init_only and not region.overlaps(INIT_AREA):
            continue
        new_regions = list[Region]()
        for r in regions:
            if r.overlaps(region):
                new_regions.extend(sub(r, region))
            else:
                new_regions.append(r)
        if action == 'on':
            new_regions.append(region)
        regions = new_regions
    return sum(r.count_points() for r in regions)


def solve() -> tuple[int, int]:
    steps = parse(read_puzzle())
    return reboot(steps, init_only=True), reboot(steps)


if __name__ == '__main__':
    print(solve())
