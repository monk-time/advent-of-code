# https://adventofcode.com/2020/day/20

import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from inspect import cleandoc
from typing import TYPE_CHECKING, ClassVar

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


type Tiles = list[list[Tile]]
type Links = defaultdict[Tile, Dir[Tile]]


@dataclass
class Dir[T]:
    t: T | None = None
    b: T | None = None
    l: T | None = None  # noqa: E741
    r: T | None = None

    DIRS: ClassVar[tuple[str, ...]] = ('t', 'b', 'l', 'r')
    OPPOSITE: ClassVar[dict[str, str]] = {
        't': 'b',
        'b': 't',
        'l': 'r',
        'r': 'l',
    }

    def __getitem__(self, key: str) -> T | None:
        return getattr(self, key)

    def __setitem__(self, key: str, value: T | None) -> None:
        setattr(self, key, value)


@dataclass(frozen=True)
class Tile:
    id: int
    data: tuple[str, ...]

    _variant_cache: ClassVar[dict['Tile', tuple['Tile', ...]]] = {}  # noqa: UP037

    def __str__(self) -> str:
        return f'Tile {self.id}:\n' + '\n'.join(self.data)

    def __repr__(self) -> str:
        return f'Tile(id={self.id})'

    @cached_property
    def edges(self) -> Dir[str]:
        return Dir(
            t=self.data[0],
            b=self.data[-1],
            l=''.join(row[0] for row in self.data),
            r=''.join(row[-1] for row in self.data),
        )

    def flip_h(self) -> Tile:
        return Tile(id=self.id, data=tuple(row[::-1] for row in self.data))

    def flip_v(self) -> Tile:
        return Tile(id=self.id, data=self.data[::-1])

    def rotate_cw(self) -> Tile:
        n = len(self.data[0])
        new_data = tuple(
            ''.join(self.data[n - 1 - x][y] for x in range(n))
            for y in range(n)
        )
        return Tile(id=self.id, data=new_data)

    def _gen_variants(self) -> Iterable[Tile]:
        tile = self
        for _ in range(4):
            yield tile
            yield tile.flip_v()
            tile = tile.rotate_cw()

    @cached_property
    def variants(self) -> tuple[Tile, ...]:
        if self not in Tile._variant_cache:
            Tile._variant_cache[self] = tuple(self._gen_variants())
        return Tile._variant_cache[self]


def parse(s: str) -> Iterable[Tile]:
    blocks = s.split('\n\n')
    for block in blocks:
        header, lines = block.split(':\n')
        tile_id = re.match(r'Tile (\d+)', header).group(1)  # type: ignore
        data = lines.split('\n')
        yield Tile(id=int(tile_id), data=tuple(data))


def find_match(
    tile: Tile, tiles: Iterable[Tile], dir_: str
) -> tuple[Tile, Tile] | tuple[None, None]:
    for tile_2 in tiles:
        for variant in tile_2.variants:
            if tile.edges[dir_] == variant.edges[Dir.OPPOSITE[dir_]]:
                return tile_2, variant
    return None, None


def connect(tiles: Sequence[Tile]) -> Links:
    links: Links = defaultdict(Dir[Tile])
    queue = {tiles[0]}
    remaining = set(tiles) - queue
    visited: set[Tile] = set()

    while queue:
        tile = queue.pop()
        remaining.discard(tile)
        for dir_ in Dir.DIRS:
            if links[tile][dir_]:
                continue
            tile_2, match = find_match(tile, remaining, dir_)
            if not tile_2 or not match:
                continue
            links[tile][dir_] = match
            links[match][Dir.OPPOSITE[dir_]] = tile
            if match not in visited:
                queue.add(match)
            if match != tile_2:
                remaining.discard(tile_2)
                remaining.add(match)
        visited.add(tile)

    return links


def fill_grid(links: Links) -> Tiles:
    def walk(tile: Tile | None, dir_: str):
        while tile:
            yield tile
            tile = links[tile][dir_]

    start = next(
        tile
        for tile, linked in links.items()
        if linked.l is None and linked.t is None
    )
    return [list(walk(row_start, 'r')) for row_start in walk(start, 'b')]


def verify_corners(grid: Tiles) -> int:
    return grid[0][0].id * grid[0][-1].id * grid[-1][0].id * grid[-1][-1].id


def stitch(grid: Tiles) -> Tile:
    tile_size = len(grid[0][0].data[0])
    return Tile(
        id=0,
        data=tuple(
            ''.join(tile.data[i][1:-1] for tile in row_tiles)
            for row_tiles in grid
            for i in range(1, tile_size - 1)
        ),
    )


MONSTER = cleandoc("""
    ..................#.
    #....##....##....###
    .#..#..#..#..#..#...
""")


def find_monsters(tile: Tile) -> int:
    for variant in tile.variants:
        text = '\n'.join(variant.data)
        width = len(tile.data[0])
        monster_width = len(MONSTER.split('\n')[0])
        regexes = [
            f'^.{{{i}}}' + MONSTER.replace('\n', f'.*\n.{{{i}}}')
            for i in range(width - monster_width + 1)
        ]
        count = sum(
            len(re.findall(r, text, flags=re.MULTILINE)) for r in regexes
        )
        if count > 0:
            # assuming monsters do not overlap
            return text.count('#') - count * MONSTER.count('#')
    return 0


def solve() -> tuple[int, int]:
    tiles = list(parse(read_puzzle()))
    grid = fill_grid(connect(tiles))
    tile = stitch(grid)
    return verify_corners(grid), find_monsters(tile)


if __name__ == '__main__':
    print(solve())
