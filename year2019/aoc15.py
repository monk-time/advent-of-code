from collections import deque
from dataclasses import replace
from enum import IntEnum
from typing import Iterable

from helpers import read_puzzle
from intcode import Computer, Intcode, parse


class Tile(IntEnum):
    WALL = 0
    EMPTY = 1
    OXYGEN = 2


Coord = tuple[int, int]
Map = dict[Coord, Tile]


def around(pos: Coord) -> Iterable[Coord]:
    x, y = pos
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def map_to_str(m: Map) -> str:
    symbols = ('#', '.', 'O', ' ')
    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    for y, x in m.keys():
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)
    xs = range(x_min, x_max + 1)
    ys = range(y_min, y_max + 1)
    return '\n'.join(
        ''.join(symbols[m.get((y, x), 3)] for x in xs) for y in ys
    )


def find_shortest_path_to_oxygen(program: Intcode) -> tuple[int, Map]:
    pos = (0, 0)
    visited: Map = {pos: Tile.EMPTY}
    queue = deque([(0, pos, Computer(program))])
    steps_to_oxygen = 0
    while queue:
        depth, pos, comp = queue.popleft()
        for command, next_pos in enumerate(around(pos), start=1):
            if next_pos in visited:
                continue
            next_comp = replace(comp)
            gen = iter(next_comp)
            next(gen)
            tile = Tile(gen.send(command))
            visited[next_pos] = tile
            if tile is not Tile.WALL:
                queue.append((depth + 1, next_pos, next_comp))
            if tile is Tile.OXYGEN:
                steps_to_oxygen = depth + 1
    return steps_to_oxygen, visited


def time_to_fill(m: Map) -> int:
    m = m.copy()
    pos_oxygen = next(pos for pos in m if m[pos] is Tile.OXYGEN)
    queue = deque([(0, pos_oxygen)])
    while queue:
        time, pos = queue.popleft()
        for next_pos in around(pos):
            if m[next_pos] is not Tile.EMPTY:
                continue
            m[next_pos] = Tile.OXYGEN
            queue.append((time + 1, next_pos))
    return time


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    part1, m = find_shortest_path_to_oxygen(program)
    print(map_to_str(m))
    return part1, time_to_fill(m)


if __name__ == '__main__':
    print(solve())
