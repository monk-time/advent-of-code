# https://adventofcode.com/2019/day/24

from collections import defaultdict
from itertools import product
from typing import TYPE_CHECKING

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator

type Coord = tuple[int, int]
type Coords = frozenset[Coord]
type AdjTable = dict[Coord, Coords]
type CoordsRec = defaultdict[int, Coords]


def around(c: Coord) -> Generator[Coord]:
    x, y = c
    yield from ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def is_in_bounds(c: Coord) -> bool:
    x, y = c
    return 0 <= x <= 4 and 0 <= y <= 4


COORDS: tuple[Coord, ...] = tuple(product(range(5), repeat=2))  # type: ignore
ADJ: AdjTable = {c: frozenset(filter(is_in_bounds, around(c))) for c in COORDS}
ADJ_TO_INNER: AdjTable = {
    (2, 1): frozenset((i, 0) for i in range(5)),  # top
    (1, 2): frozenset((0, j) for j in range(5)),  # left
    (3, 2): frozenset((4, j) for j in range(5)),  # right
    (2, 3): frozenset((i, 4) for i in range(5)),  # bottom
}
ADJ_TO_OUTER: AdjTable = {
    **{(0, j): frozenset(((1, 2),)) for j in (1, 2, 3)},
    **{(4, j): frozenset(((3, 2),)) for j in (1, 2, 3)},
    **{(i, 0): frozenset(((2, 1),)) for i in (1, 2, 3)},
    **{(i, 4): frozenset(((2, 3),)) for i in (1, 2, 3)},
    (0, 0): frozenset(((2, 1), (1, 2))),
    (4, 0): frozenset(((2, 1), (3, 2))),
    (0, 4): frozenset(((1, 2), (2, 3))),
    (4, 4): frozenset(((3, 2), (2, 3))),
}


def parse(s: str) -> Coords:
    return frozenset(
        (i, j)
        for i, line in enumerate(s.split())
        for j, ch in enumerate(line)
        if ch == '#'
    )


def will_be_a_bug(c: Coord, bugs: Coords) -> bool:
    bug_count = len(ADJ[c] & bugs)
    return bug_count == 1 or (bug_count == 2 and c not in bugs)


def update_grid(bugs: Coords) -> Coords:
    return frozenset(c for c in COORDS if will_be_a_bug(c, bugs))


def part1(bugs: Coords) -> int:
    cache = {bugs}
    while True:
        bugs = update_grid(bugs)
        if bugs in cache:
            break
        cache.add(bugs)
    return sum(2 ** (i * 5 + j) for (i, j) in bugs)


def will_be_a_bug_rec(
    c: Coord, bugs: Coords, inner: Coords, outer: Coords
) -> bool:
    adj = ADJ[c] - {(2, 2)}
    adj_inner = ADJ_TO_INNER.get(c, frozenset())
    adj_outer = ADJ_TO_OUTER.get(c, frozenset())
    bug_count = (
        len(adj & bugs) + len(adj_inner & inner) + len(adj_outer & outer)
    )
    return bug_count == 1 or (bug_count == 2 and c not in bugs)


def update_grid_rec(
    levels: CoordsRec, min_lvl: int, max_lvl: int
) -> tuple[CoordsRec, int, int]:
    next_levels: CoordsRec = defaultdict(frozenset)
    for lvl in range(min_lvl - 1, max_lvl + 2):
        outer = levels[lvl - 1]
        inner = levels[lvl + 1]
        next_level = frozenset(
            c
            for c in COORDS
            if c != (2, 2) and will_be_a_bug_rec(c, levels[lvl], inner, outer)
        )
        next_levels[lvl] = next_level
        if next_level:
            min_lvl = min(lvl, min_lvl)
            max_lvl = max(lvl, max_lvl)
    return next_levels, min_lvl, max_lvl


def part2(bugs: Coords, minutes: int = 200) -> int:
    levels: CoordsRec = defaultdict(frozenset)
    min_lvl, max_lvl = 0, 0
    levels[0] = bugs
    for _ in range(minutes):
        levels, min_lvl, max_lvl = update_grid_rec(levels, min_lvl, max_lvl)
    return sum(len(level) for level in levels.values())


def solve() -> tuple[int, int]:
    bugs = parse(read_puzzle())
    return part1(bugs), part2(bugs)


if __name__ == '__main__':
    print(solve())
