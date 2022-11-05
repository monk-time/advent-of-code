import re
from copy import deepcopy
from dataclasses import dataclass
from inspect import cleandoc
from itertools import combinations
from math import lcm
from typing import Iterable

from helpers import read_puzzle

Coord = list[int, int, int]
Planets = list['Planet']


@dataclass()
class Planet:
    pos: Coord
    vel: Coord

    def total_energy(self) -> int:
        return sum(map(abs, self.pos)) * sum(map(abs, self.vel))


def parse(s: str) -> Iterable[Planet]:
    for line in s.splitlines():
        x, y, z = map(int, re.findall(r'-?\d+', line))
        yield Planet([x, y, z], [0, 0, 0])


def apply_gravity_to_dim(dim: int, planets: Planets):
    for pl1, pl2 in combinations(planets, 2):
        if pl1.pos[dim] < pl2.pos[dim]:
            pl1.vel[dim] += 1
            pl2.vel[dim] -= 1
        elif pl1.pos[dim] > pl2.pos[dim]:
            pl1.vel[dim] -= 1
            pl2.vel[dim] += 1


def apply_velocity_to_dim(dim: int, planets: Planets):
    for pl in planets:
        pl.pos[dim] += pl.vel[dim]


def execute_time_step(planets: Planets):
    for dim in range(3):
        apply_gravity_to_dim(dim, planets)
        apply_velocity_to_dim(dim, planets)


def total_energy(planets: Planets):
    return sum(pl.total_energy() for pl in planets)


def find_loop(planets: Planets):
    periods = []
    for dim in range(3):
        pls = deepcopy(planets)
        get_hash = lambda pls_: tuple((pl.pos[dim], pl.vel[dim]) for pl in pls_)
        cache = set(get_hash(pls))
        count = -1  # no idea why but it works
        while True:
            apply_gravity_to_dim(dim, pls)
            apply_velocity_to_dim(dim, pls)
            count += 1
            hash_ = get_hash(pls)
            if hash_ in cache:
                periods.append(count)
                break
            else:
                cache.add(hash_)
    return lcm(*periods)


def solve() -> tuple[int, int]:
    planets = list(parse(read_puzzle()))
    pls = deepcopy(planets)
    for _ in range(1000):
        execute_time_step(pls)
    part1 = total_energy(pls)
    pls = deepcopy(planets)
    part2 = find_loop(pls)
    return part1, part2


if __name__ == '__main__':
    print(solve())
