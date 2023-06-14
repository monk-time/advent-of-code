from enum import StrEnum
from itertools import chain
from typing import Iterable, Literal, get_args

from helpers import read_puzzle
from intcode import Computer, parse


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
    output, s = [], ''
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
    height = max(y for _, y in tiles.keys()) + 1  # coords are 0-based
    width = max(x for x, _ in tiles.keys()) + 1
    return [
        ''.join(tiles[(x, y)] for x in range(width)) for y in range(height)
    ]


def around(pos: Coord) -> Iterable[Coord]:
    x, y = pos
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def is_intersection(tiles: TileMap, pos: Coord) -> bool:
    return tiles[pos] is Tile.FLOOR and all(
        near in tiles and tiles[near] is Tile.FLOOR for near in around(pos)
    )


def find_intersections(tiles: TileMap) -> Iterable[Coord]:
    yield from (pos for pos in tiles if is_intersection(tiles, pos))


def calibrate(tiles: TileMap) -> int:
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


def execute_full_walk(computer: Computer) -> int:
    # Hardcoded solution, solved by hand
    # by looking at the output of walk_through_all
    f_main = 'A,B,A,C,A,B,C,B,C,A'
    f_a = 'L,12,R,4,R,4,L,6'
    f_b = 'L,12,R,4,R,4,R,12'
    f_c = 'L,10,L,6,R,4'

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
    program[0] = 2
    computer = Computer(program)

    output = read_output(computer)
    tiles = parse_tiles(output)
    part1 = calibrate(tiles)

    # print(*walk_through_all(tiles), sep=',')
    part2 = execute_full_walk(computer)
    return part1, part2


if __name__ == '__main__':
    print(solve())
