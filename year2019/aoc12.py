import re
from dataclasses import dataclass
from inspect import cleandoc
from typing import Iterable
from itertools import combinations

from helpers import read_puzzle

Coord = list[int, int, int]
Planets = list['Planet']


@dataclass
class Planet:
    pos: Coord
    vel: Coord

    def total_energy(self) -> int:
        return sum(map(abs, self.pos)) * sum(map(abs, self.vel))


def parse(s: str) -> Iterable[Planet]:
    for line in s.splitlines():
        x, y, z = map(int, re.findall(r'-?\d+', line))
        yield Planet([x, y, z], [0, 0, 0])


def apply_gravity(planets: Planets):
    for pl1, pl2 in combinations(planets, 2):
        for i in range(3):
            if pl1.pos[i] < pl2.pos[i]:
                pl1.vel[i] += 1
                pl2.vel[i] -= 1
            elif pl1.pos[i] > pl2.pos[i]:
                pl1.vel[i] -= 1
                pl2.vel[i] += 1


def apply_velocity(planets: Planets):
    for pl in planets:
        for i in range(3):
            pl.pos[i] += pl.vel[i]


def execute_time_step(planets: Planets):
    apply_gravity(planets)
    apply_velocity(planets)


def total_energy(planets: Planets):
    return sum(pl.total_energy() for pl in planets)


def solve() -> tuple[int, int]:
    planets = list(parse(read_puzzle()))
    for _ in range(1000):
        execute_time_step(planets)
    return total_energy(planets), 0


if __name__ == '__main__':
    print(solve())
