from enum import StrEnum

from helpers import read_puzzle
from intcode import Intcode, parse, run_intcode


class Tile(StrEnum):
    EMPTY = ' '
    WALL = '■'
    BLOCK = '◌'
    PADDLE = '-'
    BALL = '●'

    @classmethod
    def from_index(cls, index: int):
        return cls[cls._member_names_[index]]


TileMap = dict[tuple[int, int], Tile]


def read_tiles(program: Intcode) -> TileMap:
    gen = run_intcode(program)
    tiles = {}
    while True:
        try:
            x = next(gen)
            y = next(gen)
            tile_id = next(gen)
            tiles[(x, y)] = Tile.from_index(tile_id)
        except StopIteration:
            return tiles


def print_tiles(tiles: TileMap):
    height = max(y for _, y in tiles.keys()) + 1  # coords are 0-based
    width = max(x for x, _ in tiles.keys()) + 1
    for y in range(height):
        line = ''.join(tiles[(x, y)] for x in range(width))
        print(line)


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    tiles = read_tiles(program)
    part1 = list(tiles.values()).count(Tile.BLOCK)
    print_tiles(tiles)
    return part1, 0


if __name__ == '__main__':
    print(solve())
