# https://adventofcode.com/2018/day/17

import re
from collections import defaultdict, deque
from dataclasses import dataclass

from utils_proxy import read_puzzle


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    @property
    def up(self):
        return Point(self.y - 1, self.x)

    @property
    def down(self):
        return Point(self.y + 1, self.x)

    @property
    def left(self):
        return Point(self.y, self.x - 1)

    @property
    def right(self):
        return Point(self.y, self.x + 1)


class Map(defaultdict[Point, str]):
    def __init__(self, s: str):
        super().__init__(lambda: '.')
        for line in s.splitlines():
            regex = r'([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)'
            dim1, n1, _dim2, n2, n3 = re.match(regex, line).groups()  # type: ignore
            x = int(n1)
            for y in range(int(n2), int(n3) + 1):
                self[Point(y, x) if dim1 == 'x' else Point(x, y)] = '#'

        self.min_y: int = min(self.keys(), key=lambda point: point.y).y
        self.max_y: int = max(self.keys(), key=lambda point: point.y).y

    def __str__(self):
        """Get a text representation of the map."""
        min_x = min(self.keys(), key=lambda point: point.x).x
        max_x = max(self.keys(), key=lambda point: point.x).x
        lines = [
            ''.join(self[Point(i, j)] for j in range(min_x, max_x + 1))
            for i in range(self.min_y, self.max_y + 1)
        ]
        return '\n'.join(lines)


def add_water(m: Map):  # noqa: C901
    queue = deque((Point(1, 500),))
    while queue:
        point = queue.popleft()
        # Fall down as far as possible
        while m[point] == '.' and point.y <= m.max_y:
            m[point] = '|'
            point = point.down
        if point.y > m.max_y:
            continue
        if m[point] in '~#':
            point = point.up
        if m[point.down] not in '~#':
            continue
        left, right = point, point
        # Find the left wall or edge
        while m[left.down.left] in '~#' and m[left.left] in '|.':
            left = left.left
            m[left] = '|'
        # Find the right wall or edge
        while m[right.down.right] in '~#' and m[right.right] in '|.':
            right = right.right
            m[right] = '|'
        # If surrounded by wall, fill the layer with water
        if m[left.left] not in '|.' and m[right.right] not in '|.':
            for x in range(left.x, right.x + 1):
                m[Point(point.y, x)] = '~'
            queue.append(point.up)
        # Add edges to the queue
        if m[left.left] in '|.':
            queue.append(left.left)
        if m[right.right] in '|.':
            queue.append(right.right)


def count_wet(m: Map) -> tuple[int, int]:
    wet = [x for point, x in m.items() if point.y >= m.min_y]
    sand = sum(x == '|' for x in wet)
    water = sum(x == '~' for x in wet)
    return sand + water, water


def solve():
    m = Map(read_puzzle())
    add_water(m)
    return count_wet(m)


if __name__ == '__main__':
    print(solve())
