# https://adventofcode.com/2018/day/13

from collections.abc import Iterable
from itertools import product
from typing import NamedTuple

from helpers import read_puzzle


class Cart(NamedTuple):
    x: int
    y: int
    dir: str  # >, <, ^, v
    turn: int  # 0 (left), 1 (straight), 2 (right)


def parse(s: str) -> tuple[list[Cart], list[str]]:
    carts = []
    tracks = s.splitlines()
    m, n = len(tracks), len(tracks[0])
    for i, j in product(range(m), range(n)):
        if tracks[i][j] in '><^v':
            carts.append(Cart(x=j, y=i, dir=tracks[i][j], turn=0))
            # Carts always start on straight paths
            path_under = '-' if tracks[i][j] in '><' else '|'
            tracks[i] = tracks[i][:j] + path_under + tracks[i][j + 1 :]
    return carts, tracks


def look_ahead(c: Cart) -> tuple[int, int]:
    return (
        c.x + (1 if c.dir == '>' else -1 if c.dir == '<' else 0),
        c.y + (1 if c.dir == 'v' else -1 if c.dir == '^' else 0),
    )


cart_states = {
    # Straight
    '>-': (1, 0, '>'),
    '<-': (-1, 0, '<'),
    '>1': (1, 0, '>'),
    '<1': (-1, 0, '<'),
    'v|': (0, 1, 'v'),
    '^|': (0, -1, '^'),
    'v1': (0, 1, 'v'),
    '^1': (0, -1, '^'),
    # Clockwise turn
    '^/': (0, -1, '>'),
    '>\\': (1, 0, 'v'),
    '^2': (0, -1, '>'),
    '>2': (1, 0, 'v'),
    'v/': (0, 1, '<'),
    '<\\': (-1, 0, '^'),
    'v2': (0, 1, '<'),
    '<2': (-1, 0, '^'),
    # Counterclockwise turn
    '>/': (1, 0, '^'),
    '^\\': (0, -1, '<'),
    '>0': (1, 0, '^'),
    '^0': (0, -1, '<'),
    '</': (-1, 0, 'v'),
    'v\\': (0, 1, '>'),
    '<0': (-1, 0, 'v'),
    'v0': (0, 1, '>'),
}


def move(c: Cart, ahead: str) -> Cart:
    key = c.dir + (ahead if ahead != '+' else str(c.turn))
    turn_new = c.turn if ahead != '+' else (c.turn + 1) % 3
    dx, dy, dir_new = cart_states[key]
    return Cart(c.x + dx, c.y + dy, dir_new, turn_new)


def next_tick(carts_prev: list[Cart], tracks: list[str]):
    carts_prev = carts_prev.copy()
    carts_next, crashes = [], []
    while carts_prev:
        cart = carts_prev.pop(0)
        x, y = look_ahead(cart)
        # A cart can crash into a cart that either is yet to move or has moved
        for carts in [carts_prev, carts_next]:
            victim = next((c for c in carts if (c.x, c.y) == (x, y)), None)
            if victim:
                crashes.append((x, y))
                carts.remove(victim)
                break
        else:  # no break, i.e. no crash
            carts_next.append(move(cart, tracks[y][x]))

    return sorted(carts_next, key=lambda c: (c.y, c.x)), tracks, crashes


def emulate(carts: list[Cart], tracks: list[str]) -> Iterable[str]:
    had_first_crash = False
    answer = lambda a, b: f'{a},{b}'
    while len(carts) > 1:
        carts, tracks, crashes = next_tick(carts, tracks)
        if crashes and not had_first_crash:
            yield answer(*crashes[0])  # first crash
            had_first_crash = True
    # Yield coords of the last cart
    yield (answer(carts[0].x, carts[0].y) if carts else '')


def solve():
    return tuple(emulate(*parse(read_puzzle(stripchars='\n'))))


if __name__ == '__main__':
    print(solve())
