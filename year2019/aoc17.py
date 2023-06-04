from enum import StrEnum
from typing import Iterable
from helpers import read_puzzle
from intcode import Computer, Intcode, parse


class Tile(StrEnum):
    EMPTY = '.'
    FLOOR = '#'
    LEFT = '<'
    RIGHT = '>'
    UP = '^'
    DOWN = 'v'


Coord = tuple[int, int]
TileMap = dict[Coord, Tile]

# R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2
# A       B           C       B           A       C
# xxyyxzwyyxxxzw
# A B  C B  A C
# A = xx, B == yyx, C = zw

def read_tiles(program: Intcode) -> TileMap:
    gen = iter(Computer(program))
    tiles = {}
    x = y = 0
    while True:
        try:
            tile_str = chr(next(gen))
            if tile_str == '\n':
                y += 1
                x = 0
            else:
                tiles[(x, y)] = Tile(tile_str)
                x += 1
        except StopIteration:
            return tiles


def print_tiles(tiles: TileMap):
    height = max(y for _, y in tiles.keys()) + 1  # coords are 0-based
    width = max(x for x, _ in tiles.keys()) + 1
    line = '\n'.join(
        ''.join(tiles[(x, y)] for x in range(width)) for y in range(height)
    )
    print(line)


def around(coord: Coord) -> Iterable[Coord]:
    x, y = coord
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def is_intersection(coord: Coord, tiles: TileMap) -> bool:
    return tiles[coord] is Tile.FLOOR and all(
        near in tiles and tiles[near] is Tile.FLOOR for near in around(coord)
    )


def find_intersections(tiles: TileMap) -> Iterable[Coord]:
    yield from (coord for coord in tiles if is_intersection(coord, tiles))


def calibrate(tiles: TileMap) -> int:
    return sum(x * y for x, y in find_intersections(tiles))


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    tiles = read_tiles(program)
    print_tiles(tiles)
    return calibrate(tiles), 0


if __name__ == '__main__':
    print(solve())
