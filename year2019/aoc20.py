# https://adventofcode.com/2019/day/20

from collections import defaultdict, deque
from collections.abc import Generator
from operator import add, sub
from string import ascii_uppercase
from typing import Self

from helpers import read_puzzle

type Coord = tuple[int, int]


def around(pos: Coord) -> Generator[Coord, None, None]:
    x, y = pos
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def is_portal(s: str) -> bool:
    return s in ascii_uppercase


class TileMap:
    def __init__(self, tiles: dict[Coord, str]) -> None:
        self.tiles = tiles
        self.portals = self._find_portals()
        self.connected: dict[Coord, Coord] = {}
        for coords in self.portals.values():
            if len(coords) != 2:
                continue
            pos1, pos2 = coords
            self.connected.update(((pos1, pos2), (pos2, pos1)))
        self.exits: list[Coord] = []
        for portal in ('AA', 'ZZ'):
            portal_pos = next(iter(self.portals[portal]))
            self.exits.append(portal_pos)

    def _find_portals(self) -> defaultdict[str, set[Coord]]:
        portals: defaultdict[str, set[Coord]] = defaultdict(set)
        for pos, tile in self.tiles.items():
            if tile != '.':
                continue
            near = list(around(pos))
            portal_bools = [is_portal(self.tiles.get(t, ' ')) for t in near]
            if True not in portal_bools:
                continue
            portal_pos1 = near[portal_bools.index(True)]
            delta: Coord = tuple(map(sub, portal_pos1, pos))
            portal_pos2 = tuple(map(add, portal_pos1, delta))
            letters = [self.tiles[portal_pos1], self.tiles[portal_pos2]]
            if delta in {(-1, 0), (0, -1)}:
                letters.reverse()
            portals[''.join(letters)].add(pos)
        return portals

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls({
            (x + 1, y + 1): char
            for y, line in enumerate(s.split('\n'))
            for x, char in enumerate(line)
        })

    def step(self, pos: Coord) -> Generator[Coord, None, None]:
        if pos in self.connected:
            yield self.connected[pos]
        for next_pos in around(pos):
            if next_pos in self.tiles and self.tiles[next_pos] == '.':
                yield next_pos


def find_min_path_len(tile_map: TileMap) -> int:
    visited: set[Coord] = {tile_map.exits[0]}
    queue: deque[tuple[Coord, int]] = deque([(tile_map.exits[0], 0)])
    while queue:
        pos, steps = queue.popleft()
        for next_pos in tile_map.step(pos):
            if next_pos in visited:
                continue
            if next_pos == tile_map.exits[1]:
                return steps + 1
            queue.append((next_pos, steps + 1))
            visited.add(next_pos)
    return 0


def solve() -> tuple[int, int]:
    tile_map = TileMap.from_str(read_puzzle(stripchars=''))
    return find_min_path_len(tile_map), 0


if __name__ == '__main__':
    print(solve())
