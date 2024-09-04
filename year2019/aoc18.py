# https://adventofcode.com/2019/day/18

from bisect import insort
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
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


def find_reachable_keys_bfs(
    tiles: TileMap, start: Coord
) -> Iterable[tuple[str, int, list[str]]]:
    visited: set[Coord] = {start}
    queue: deque[tuple[Coord, int, list[str]]] = deque([(start, 0, [])])
    while queue:
        pos, steps, req_keys = queue.popleft()
        for next_pos in around(pos):
            tile = tiles[next_pos]
            if next_pos in visited or tile.is_wall():
                continue
            if tile.is_key():
                yield (tile.value, steps + 1, req_keys)
                continue
            next_req_keys = req_keys
            if tile.is_door():
                next_req_keys = [*req_keys, tile.value.lower()]
            queue.append((next_pos, steps + 1, next_req_keys))
            visited.add(next_pos)


def shortest_path_len(tiles: TileMap) -> int:
    start = next(c for c, tile in tiles.items() if tile.value == '@')
    start_graph = sorted(find_reachable_keys_bfs(tiles, start))
    key_graph = {
        tile.value: sorted(find_reachable_keys_bfs(tiles, pos))
        for pos, tile in tiles.items()
        if tile.is_key()
    }
    queue: deque[tuple[str, int, list[str]]] = deque(
        (key, steps, [key]) for key, steps, doors in start_graph if not doors
    )
    visited = {}
    while queue:
        key, steps, keys = queue.popleft()
        reachable_keys = key_graph[key]
        for next_key, steps_to_key, doors in reachable_keys:
            if not all(door in keys for door in doors):
                continue
            next_keys = [*keys, next_key] if next_key not in keys else keys
            next_steps = steps + steps_to_key
            if len(next_keys) == len(key_graph):
                return next_steps
            visited_key = (next_key, frozenset(next_keys))
            if visited_key in visited and next_steps >= visited[visited_key]:
                continue
            insort(queue, (next_key, next_steps, next_keys), key=itemgetter(1))
            visited[visited_key] = next_steps
    return 0


def solve() -> tuple[int, int]:
    tiles = parse(read_puzzle())
    return shortest_path_len(tiles), 0


if __name__ == '__main__':
    print(solve())
