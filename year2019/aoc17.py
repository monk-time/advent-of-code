# https://adventofcode.com/2019/day/17

import re
from enum import StrEnum
from typing import TYPE_CHECKING, Literal, cast, get_args

from helpers import read_puzzle
from intcode import Computer, Intcode, parse

if TYPE_CHECKING:
    from collections.abc import Iterable


class Tile(StrEnum):
    EMPTY = '.'
    FLOOR = '#'
    LEFT = '<'
    RIGHT = '>'
    UP = '^'
    DOWN = 'v'
    OFF = 'X'

    def is_direction(self):
        return self in get_args(Direction)


Direction = Literal[Tile.LEFT, Tile.RIGHT, Tile.UP, Tile.DOWN]

Coord = tuple[int, int]
TileMap = dict[Coord, Tile]


def read_output(computer: Computer) -> list[str]:
    gen = iter(computer)
    output: list[str] = []
    s = ''
    while True:
        tile_char = chr(next(gen))
        if tile_char == '\n':
            if s:
                output.append(s)
                s = ''
            else:
                return output
        else:
            s += tile_char


def parse_tiles(lines: list[str]) -> TileMap:
    return {
        (x, y): Tile(char)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
    }


def render_tiles(tiles: TileMap) -> list[str]:
    height = max(y for _, y in tiles) + 1  # coords are 0-based
    width = max(x for x, _ in tiles) + 1
    return [''.join(tiles[x, y] for x in range(width)) for y in range(height)]


def around(pos: Coord) -> Iterable[Coord]:
    x, y = pos
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def is_intersection(tiles: TileMap, pos: Coord) -> bool:
    return tiles[pos] is Tile.FLOOR and all(
        near in tiles and tiles[near] is Tile.FLOOR for near in around(pos)
    )


def find_intersections(tiles: TileMap) -> Iterable[Coord]:
    yield from (pos for pos in tiles if is_intersection(tiles, pos))


def calibrate(program: Intcode) -> int:
    tiles = parse_tiles(read_output(Computer(program)))
    return sum(x * y for x, y in find_intersections(tiles))


def step(pos: Coord, direction: Direction):
    x, y = pos
    match direction:
        case Tile.LEFT:
            return x - 1, y
        case Tile.RIGHT:
            return x + 1, y
        case Tile.UP:
            return x, y - 1
        case Tile.DOWN:
            return x, y + 1


DIRS_ORDERED = (Tile.UP, Tile.RIGHT, Tile.DOWN, Tile.LEFT)


def turn(direction: Direction):
    index = DIRS_ORDERED.index(direction)
    return DIRS_ORDERED[(index - 1) % 4], DIRS_ORDERED[(index + 1) % 4]


def walk_through_all(tiles: TileMap) -> Iterable[int | str]:
    pos = next(pos for pos, tile in tiles.items() if tile.is_direction())
    direction = tiles[pos]
    direction = cast('Direction', direction)
    steps = 0
    while True:
        next_pos = step(pos, direction)
        if next_pos in tiles and tiles[next_pos] is Tile.FLOOR:
            pos = next_pos
            steps += 1
            continue
        if steps:
            yield steps
        steps = 1
        left_dir, right_dir = turn(direction)
        left_pos = step(pos, left_dir)
        right_pos = step(pos, right_dir)
        if right_pos in tiles and tiles[right_pos] is Tile.FLOOR:
            pos = right_pos
            direction = right_dir
            yield 'R'
        elif left_pos in tiles and tiles[left_pos] is Tile.FLOOR:
            pos = left_pos
            direction = left_dir
            yield 'L'
        else:
            break


def execute_full_walk(program: Intcode) -> int:
    computer = Computer(program)
    computer.program[0] = 2
    tiles = parse_tiles(read_output(computer))
    path = ','.join(map(str, walk_through_all(tiles)))
    print(path)

    path += ','
    regex = r'^(.{1,21})\1*(.{1,21})(?:\1|\2)*(.{1,21})(?:\1|\2|\3)*$'
    match = re.match(regex, path)
    assert match is not None
    f_a, f_b, f_c = (g[:-1] for g in match.groups())
    f_main = path.replace(f_a, 'A').replace(f_b, 'B').replace(f_c, 'C')[:-1]
    print(f'Main function: {f_main}')
    print(f'Function A: {f_a}')
    print(f'Function B: {f_b}')
    print(f'Function C: {f_c}')

    gen = iter(computer)
    for f in (f_main, f_a, f_b, f_c):
        while chr(next(gen)) != '\n':
            pass
        next(gen)
        for x in f:
            gen.send(ord(x))
        gen.send(ord('\n'))
    while chr(next(gen)) != '\n':
        pass
    next(gen)
    gen.send(ord('n'))
    gen.send(ord('\n'))
    read_output(computer)
    return next(gen)


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    return calibrate(program), execute_full_walk(program)


if __name__ == '__main__':
    print(solve())
