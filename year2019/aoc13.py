from helpers import read_puzzle
from year2019.aoc09 import Intcode, run_intcode, parse

tiles_to_symbol = {
    0: ' ',
    1: '■',
    2: '◌',
    3: '-',
    4: '●',
}

Tiles = dict[tuple[int, int], int]


def draw_tiles(program: Intcode) -> Tiles:
    gen = run_intcode(program)
    tiles = {}
    while True:
        try:
            x = next(gen)
            y = next(gen)
            tile_id = next(gen)
            tiles[(x, y)] = tile_id
        except StopIteration:
            return tiles


def print_tiles(tiles: Tiles):
    height = max(y for _, y in tiles.keys()) + 1  # coords are 0-based
    width = max(x for x, _ in tiles.keys()) + 1
    for y in range(height):
        line = ''
        for x in range(width):
            tile = tiles[(x, y)]
            line += tiles_to_symbol[tile]
        print(line)


def solve() -> tuple[int, int]:
    program = parse(read_puzzle())
    tiles = draw_tiles(program)
    part1 = list(tiles.values()).count(2)
    # print_tiles(tiles)
    return part1, 0


if __name__ == '__main__':
    print(solve())
