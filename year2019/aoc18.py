# https://adventofcode.com/2019/day/18

from bisect import insort
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache
from operator import itemgetter
from string import ascii_lowercase, ascii_uppercase

from frozendict import frozendict

from helpers import read_puzzle


@dataclass(frozen=True)
class Tile:
    value: str

    def is_wall(self) -> bool:
        return self.value == '#'

    def is_key(self) -> bool:
        return self.value in ascii_lowercase

    def is_door(self) -> bool:
        return self.value in ascii_uppercase


type Coord = tuple[int, int]
type TileMap = frozendict[Coord, Tile]


def around(pos: Coord) -> Iterable[Coord]:
    x, y = pos
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def parse(s: str) -> TileMap:
    return frozendict(
        ((x, y), Tile(char))
        for y, line in enumerate(s.split())
        for x, char in enumerate(line)
    )


@cache
def find_reachable_keys_bfs(
    tiles: TileMap, start: Coord, keys: frozenset[str]
) -> dict[str, int]:
    visited: set[Coord] = {start}
    queue: deque[tuple[Coord, int]] = deque([(start, 0)])
    reachable_keys: dict[str, int] = {}
    while queue:
        prev_pos, steps = queue.popleft()
        steps += 1
        for pos in around(prev_pos):
            tile = tiles[pos]
            if (
                pos in visited
                or tile.is_wall()
                or (tile.is_door() and tile.value.lower() not in keys)
            ):
                continue
            if tile.is_key() and tile.value not in keys:
                reachable_keys[tile.value] = steps
                continue
            queue.append((pos, steps))
            visited.add(pos)
    return reachable_keys


def shortest_path_len(tiles: TileMap) -> int:
    start = next(c for c, tile in tiles.items() if tile.value == '@')
    key_dict = {
        tile.value: pos for pos, tile in tiles.items() if tile.is_key()
    }
    queue: deque[tuple[Coord, int, list[str]]] = deque([(start, 0, [])])
    shortest_path: list[str] = []
    while queue:
        pos, steps, keys = queue.popleft()
        reachable_keys = find_reachable_keys_bfs(tiles, pos, frozenset(keys))
        if not reachable_keys:
            print(shortest_path)
            return steps
        for key, steps_to_key in reachable_keys.items():
            item_to_queue = (key_dict[key], steps + steps_to_key, [*keys, key])
            insort(queue, item_to_queue, key=itemgetter(1))
    return 0


def solve() -> tuple[int, int]:
    tiles = parse(read_puzzle())
    return shortest_path_len(tiles), 0


if __name__ == '__main__':
    print(solve())
