# https://adventofcode.com/2020/day/12

from collections.abc import Callable
from functools import partial

from helpers import read_puzzle

type Move = tuple[str, int]
type Coord = complex
type Actions = dict[str, Callable[[int, Coord, Coord], tuple[Coord, Coord]]]

ACTIONS: Actions = {
    'N': lambda n, c, waypoint: (c + n * 1j, waypoint),
    'S': lambda n, c, waypoint: (c - n * 1j, waypoint),
    'E': lambda n, c, waypoint: (c + n, waypoint),
    'W': lambda n, c, waypoint: (c - n, waypoint),
    'L': lambda n, c, waypoint: (c, waypoint * ((+1j) ** (n // 90))),
    'R': lambda n, c, waypoint: (c, waypoint * ((-1j) ** (n // 90))),
    'F': lambda n, c, waypoint: (c + n * waypoint, waypoint),
}


def parse(s: str) -> list[Move]:
    return [(line[0], int(line[1:])) for line in s.split()]


def execute(
    moves: list[Move], waypoint: Coord, *, move_waypoint: bool = False
) -> int:
    c = 0j
    for action, n in moves:
        if move_waypoint and action in 'NSEW':
            waypoint, c = ACTIONS[action](n, waypoint, c)
        else:
            c, waypoint = ACTIONS[action](n, c, waypoint)
    return int(abs(c.real) + abs(c.imag))


part1 = partial(execute, waypoint=1 + 0j)
part2 = partial(execute, waypoint=10 + 1j, move_waypoint=True)


def solve() -> tuple[int, int]:
    moves = parse(read_puzzle())
    return part1(moves), part2(moves)


if __name__ == '__main__':
    print(solve())
