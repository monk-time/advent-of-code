# https://adventofcode.com/2019/day/18

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from string import ascii_lowercase, ascii_uppercase
from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


@dataclass(frozen=True)
class Tile:
    value: str

    def is_wall(self) -> bool:
        return self.value == '#'

    def is_key(self) -> bool:
        return self.value in ascii_lowercase

    def is_door(self) -> bool:
        return self.value in ascii_uppercase

    def is_start(self) -> bool:
        return self.value == '@'


type Coord = tuple[int, int]
type TileMap = dict[Coord, Tile]


def around(pos: Coord) -> Iterable[Coord]:
    x, y = pos
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def parse(s: str) -> TileMap:
    return {
        (x, y): Tile(char)
        for y, line in enumerate(s.split())
        for x, char in enumerate(line)
    }


def get_start(tiles: TileMap) -> Coord:
    return next(c for c, tile in tiles.items() if tile.is_start())


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
    key_graph = {
        tile.value: sorted(find_reachable_keys_bfs(tiles, pos))
        for pos, tile in tiles.items()
        if tile.is_key() or tile.is_start()
    }
    queue: list[tuple[int, str, list[str]]] = [(0, '@', [])]
    visited = {}
    while queue:
        steps, key, keys = heappop(queue)
        reachable_keys = key_graph[key]
        for next_key, steps_to_key, doors in reachable_keys:
            # First condition is a hack for part 2
            if any(door in key_graph and door not in keys for door in doors):
                continue
            next_keys = [*keys, next_key] if next_key not in keys else keys
            next_steps = steps + steps_to_key
            if len(next_keys) == len(key_graph) - 1:  # compensate for @
                return next_steps
            key_state = (next_key, frozenset(next_keys))
            if key_state in visited and next_steps >= visited[key_state]:
                continue
            heappush(queue, (next_steps, next_key, next_keys))
            visited[key_state] = next_steps
    return 0


def shortest_path_len_by_quadrants(tiles: TileMap) -> int:
    def filter_by_pred(pred: Callable[[int, int], bool]):
        return {(i, j): tile for (i, j), tile in tiles.items() if pred(i, j)}

    # Relies on a falsy assumption that in a quadrant we can ignore doors
    # that don't have keys in it.
    start = get_start(tiles)
    wall_offsets = ((-1, 0), (0, -1), (0, 0), (0, 1), (1, 0))
    for i, j in wall_offsets:
        tiles[start[0] + i, start[1] + j] = Tile('#')
    start_offsets = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    for i, j in start_offsets:
        tiles[start[0] + i, start[1] + j] = Tile('@')
    quadrants: list[TileMap] = [
        filter_by_pred(lambda i, j: i <= start[0] and j <= start[1]),
        filter_by_pred(lambda i, j: i >= start[0] and j <= start[1]),
        filter_by_pred(lambda i, j: i <= start[0] and j >= start[1]),
        filter_by_pred(lambda i, j: i >= start[0] and j >= start[1]),
    ]
    return sum(shortest_path_len(quadrant) for quadrant in quadrants)


def solve() -> tuple[int, int]:
    tiles = parse(read_puzzle())
    return (
        shortest_path_len(tiles),
        shortest_path_len_by_quadrants(tiles),
    )


if __name__ == '__main__':
    print(solve())
