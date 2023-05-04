import os
from enum import StrEnum

from helpers import read_puzzle
from intcode import Computer, Intcode, parse


class Tile(StrEnum):
    EMPTY = ' '
    WALL = '■'
    BLOCK = '◌'
    PADDLE = '—'
    BALL = '●'

    @classmethod
    def from_index(cls, index: int):
        return cls[cls._member_names_[index]]


Coord = tuple[int, int]
TileMap = dict[Coord, Tile]


def read_tiles(program: Intcode) -> TileMap:
    gen = iter(Computer(program))
    tiles = {}
    while True:
        try:
            x, y, tile_id = [next(gen) for _ in range(3)]
            tiles[(x, y)] = Tile.from_index(tile_id)
        except StopIteration:
            return tiles


def print_tiles(tiles: TileMap):
    os.system('cls')
    height = max(y for _, y in tiles.keys()) + 1  # coords are 0-based
    width = max(x for x, _ in tiles.keys()) + 1
    line = '\n'.join(
        ''.join(tiles[(x, y)] for x in range(width)) for y in range(height)
    )
    print(line)


def find_paddle_and_ball(tiles: TileMap) -> Coord:
    paddle, ball = None, None
    for coord, tile in tiles.items():
        if tile is Tile.BALL:
            ball = coord
        elif tile is Tile.PADDLE:
            paddle = coord
    return paddle, ball


def run_game(program: Intcode):
    gen = iter(Computer(program))
    tiles: TileMap = {}
    score = 0
    while True:
        try:
            x = next(gen)
            if x is None:
                # print_tiles(tiles)
                paddle, ball = find_paddle_and_ball(tiles)
                x_diff = ball[0] - paddle[0]
                joystick_pos = -1 if x_diff < 0 else (1 if x_diff > 0 else 0)
                x = gen.send(joystick_pos)
            y = next(gen)
            tile_id = next(gen)
            if (x, y) == (-1, 0):
                score = tile_id
                continue
            tiles[(x, y)] = Tile.from_index(tile_id)
        except StopIteration:
            return score


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    tiles = read_tiles(program)
    part1 = list(tiles.values()).count(Tile.BLOCK)
    program[0] = 2
    part2 = run_game(program)
    return part1, part2


if __name__ == '__main__':
    print(solve())
