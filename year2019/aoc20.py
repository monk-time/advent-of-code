# https://adventofcode.com/2019/day/20

from collections import defaultdict, deque
from dataclasses import dataclass
from operator import add, itemgetter, sub
from string import ascii_uppercase
from typing import TYPE_CHECKING, Self

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator

type Coord = tuple[int, int]
type MoveInfo = tuple[Coord, int]  # 1/-1 if on outer/inner edge; 0 otherwise
type Tiles = dict[Coord, str]


def around(pos: Coord) -> Generator[Coord]:
    x, y = pos
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


@dataclass(frozen=True)
class Portal:
    pos: Coord
    next_pos: Coord | None
    label: str
    outer: bool


class TileMap:
    def __init__(self, tiles: Tiles) -> None:
        self.tiles = tiles
        self.portals: dict[Coord, Portal] = self._find_portals(tiles)
        self.exits: list[Coord] = [
            next(p.pos for p in self.portals.values() if p.label == exit_label)
            for exit_label in ('AA', 'ZZ')
        ]

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls({
            (x + 1, y + 1): char
            for y, line in enumerate(s.split('\n'))
            for x, char in enumerate(line)
        })

    @classmethod
    def _find_portals(cls, tiles: Tiles) -> dict[Coord, Portal]:
        portal_coords: defaultdict[str, set[Coord]] = defaultdict(set)
        for pos, tile in tiles.items():
            if tile != '.':
                continue
            label = cls._get_portal_label(tiles, pos)
            if label is None:
                continue
            portal_coords[label].add(pos)
        x_max, y_max = [max(map(itemgetter(i), tiles)) for i in range(2)]
        x_edges, y_edges = {3, x_max - 2}, {3, y_max - 2}
        is_outer = lambda pos: pos[0] in x_edges or pos[1] in y_edges
        portals: dict[Coord, Portal] = {}
        for label, coord_set in portal_coords.items():
            if len(coord_set) != 2:
                coord = next(iter(coord_set))
                portals[coord] = Portal(coord, None, label, outer=True)
                continue
            c1, c2 = list(coord_set)
            portals[c1] = Portal(c1, c2, label, is_outer(c1))
            portals[c2] = Portal(c2, c1, label, is_outer(c2))
        return portals

    @classmethod
    def _get_portal_label(cls, tiles: Tiles, pos: Coord) -> str | None:
        near = list(around(pos))
        portal_bools = [tiles.get(t, ' ') in ascii_uppercase for t in near]
        if True not in portal_bools:
            return None
        portal_pos1 = near[portal_bools.index(True)]
        delta: Coord = tuple(map(sub, portal_pos1, pos, strict=True))
        portal_pos2 = tuple(map(add, portal_pos1, delta, strict=True))
        letters = [tiles[portal_pos1], tiles[portal_pos2]]
        if delta in {(-1, 0), (0, -1)}:
            letters.reverse()
        return ''.join(letters)

    def step(self, pos: Coord) -> Generator[MoveInfo]:
        if pos in self.portals:
            portal = self.portals[pos]
            if portal.next_pos is not None:
                yield portal.next_pos, -1 if portal.outer else 1
        for next_pos in around(pos):
            if next_pos in self.tiles and self.tiles[next_pos] == '.':
                yield next_pos, 0


def find_min_path_len(tile_map: TileMap, *, recursive: bool = False) -> int:
    visited: set[MoveInfo] = {(tile_map.exits[0], 0)}
    queue: deque[tuple[Coord, int, int]] = deque([(tile_map.exits[0], 0, 0)])
    while queue:
        pos, steps, depth = queue.popleft()
        for next_pos, depth_delta in tile_map.step(pos):
            next_depth = depth + depth_delta
            if (next_pos, next_depth) in visited or next_depth < 0:
                continue
            next_steps = steps + 1
            visited.add((next_pos, next_depth))
            if next_pos == tile_map.exits[1] and (not recursive or depth == 0):
                return next_steps
            queue.append((next_pos, next_steps, next_depth))
    return 0


def solve() -> tuple[int, int]:
    tile_map = TileMap.from_str(read_puzzle(stripchars=''))
    return (
        find_min_path_len(tile_map),
        find_min_path_len(tile_map, recursive=True),
    )


if __name__ == '__main__':
    print(solve())
