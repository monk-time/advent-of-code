# https://adventofcode.com/2018/day/20

from collections import deque
from typing import TYPE_CHECKING

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

Point = tuple[int, int]
Map = dict[Point, str]

turns: dict[str, Callable[[Point], tuple[Point, Point, str]]] = {
    'N': lambda t: ((t[0] - 2, t[1]), (t[0] - 1, t[1]), '-'),
    'S': lambda t: ((t[0] + 2, t[1]), (t[0] + 1, t[1]), '-'),
    'W': lambda t: ((t[0], t[1] - 2), (t[0], t[1] - 1), '|'),
    'E': lambda t: ((t[0], t[1] + 2), (t[0], t[1] + 1), '|'),
}


def around(pos: tuple[int, int]) -> Iterable[Point]:
    y, x = pos
    yield from (
        (y - 1, x - 1),
        (y - 1, x),
        (y - 1, x + 1),
        (y, x - 1),
        (y, x + 1),
        (y + 1, x - 1),
        (y + 1, x),
        (y + 1, x + 1),
    )


def adj_rooms_and_doors(pos: tuple[int, int]) -> Iterable[tuple[Point, Point]]:
    y, x = pos
    yield from (
        ((y - 2, x), (y - 1, x)),
        ((y, x - 2), (y, x - 1)),
        ((y, x + 2), (y, x + 1)),
        ((y + 2, x), (y + 1, x)),
    )


def parse_map(s: str) -> Map:
    pos = (0, 0)
    m: Map = {pos: 'X'}
    for pos2 in around(pos):
        m[pos2] = '#'
    stack: list[Point] = []
    for ch in s[1:-1]:
        if ch in 'NWES':
            pos, door_pos, door = turns[ch](pos)
            m[pos] = '.'
            m[door_pos] = door
            for pos2 in around(pos):
                if pos2 not in m:
                    m[pos2] = '#'
        elif ch == '(':
            stack.append(pos)
        elif ch == '|':
            pos = stack[-1]
        elif ch == ')':
            pos = stack.pop()
    return m


def map_to_str(m: Map) -> str:
    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    for y, x in m:
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)
    xs = range(x_min, x_max + 1)
    ys = range(y_min, y_max + 1)
    return '\n'.join(''.join(m.get((y, x), ' ') for x in xs) for y in ys)


def max_doors_in_shortest_path(m: Map) -> tuple[int, int]:
    pos, n_doors = (0, 0), 0
    visited: dict[Point, int] = {pos: n_doors}
    queue: deque[tuple[Point, int]] = deque([(pos, n_doors)])
    while queue:
        pos, n_doors = queue.popleft()
        for room, door in adj_rooms_and_doors(pos):
            if m[door] not in '-|' or room in visited:
                continue
            visited[room] = n_doors + 1
            queue.append((room, n_doors + 1))
    return n_doors, sum(n >= 1000 for n in visited.values())


def solve():
    m = parse_map(read_puzzle())
    return max_doors_in_shortest_path(m)


if __name__ == '__main__':
    print(solve())
