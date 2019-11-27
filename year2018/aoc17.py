import re
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Tuple

from helpers import read_puzzle


@dataclass(frozen=True)
class P:
    y: int
    x: int

    @property
    def up(self):
        return P(self.y - 1, self.x)

    @property
    def down(self):
        return P(self.y + 1, self.x)

    @property
    def left(self):
        return P(self.y, self.x - 1)

    @property
    def right(self):
        return P(self.y, self.x + 1)


class Map(defaultdict):
    def __init__(self, s: str):
        super().__init__(lambda: '.')
        for line in s.splitlines():
            regex = r'([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)'
            dim1, n1, dim2, n2, n3 = re.match(regex, line).groups()
            x = int(n1)
            for y in range(int(n2), int(n3) + 1):
                self[P(y, x) if dim1 == 'x' else P(x, y)] = '#'

        self.min_y = min(self.keys(), key=lambda p: p.y).y
        self.max_y = max(self.keys(), key=lambda p: p.y).y

    def __str__(self):
        """Get a text representation of the map."""
        min_x = min(self.keys(), key=lambda p: p.x).x
        max_x = max(self.keys(), key=lambda p: p.x).x
        lines = [''.join(self[P(i, j)]
                         for j in range(min_x, max_x + 1))
                 for i in range(self.min_y, self.max_y + 1)]
        return '\n'.join(lines)


def add_water(m: Map):
    queue = deque((P(1, 500),))
    while queue:
        p = queue.popleft()
        # Fall down as far as possible
        while m[p] == '.' and p.y <= m.max_y:
            m[p] = '|'
            p = p.down
        if p.y > m.max_y:
            continue
        if m[p] in '~#':
            p = p.up
        if m[p.down] not in '~#':
            continue
        l, r = p, p
        # Find the left wall or edge
        while m[l.down.left] in '~#' and m[l.left] in '|.':
            l = l.left
            m[l] = '|'
        # Find the right wall or edge
        while m[r.down.right] in '~#' and m[r.right] in '|.':
            r = r.right
            m[r] = '|'
        # If surrounded by wall, fill the layer with water
        if m[l.left] not in '|.' and m[r.right] not in '|.':
            for x in range(l.x, r.x + 1):
                m[P(p.y, x)] = '~'
            queue.append(p.up)
        # Add edges to the queue
        if m[l.left] in '|.':
            queue.append(l.left)
        if m[r.right] in '|.':
            queue.append(r.right)


def count_wet(m: Map) -> Tuple[int, int]:
    wet = [x for p, x in m.items() if p.y >= m.min_y]
    sand = sum(x == '|' for x in wet)
    water = sum(x == '~' for x in wet)
    return sand + water, water


def solve():
    m = Map(read_puzzle())
    add_water(m)
    return count_wet(m)


if __name__ == '__main__':
    print(solve())
