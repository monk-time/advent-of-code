# https://adventofcode.com/2021/day/25
# tags: #grid #cellular-automaton

from dataclasses import dataclass
from itertools import count

from utils_proxy import read_puzzle

type Coord = tuple[int, int]


@dataclass(frozen=True)
class State:
    width: int
    height: int
    east: frozenset[Coord]
    south: frozenset[Coord]


def parse(s: str) -> State:
    lines = s.splitlines()
    east, south = set[Coord](), set[Coord]()
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch == 'v':
                south.add((i, j))
            elif ch == '>':
                east.add((i, j))
    return State(
        width=len(lines[0]),
        height=len(lines),
        east=frozenset(east),
        south=frozenset(south),
    )


def step(state: State) -> State:
    w, h = state.width, state.height
    east = frozenset(
        c
        if (c := (i, (j + 1) % w)) not in state.east and c not in state.south
        else (i, j)
        for i, j in state.east
    )
    south = frozenset(
        c
        if (c := ((i + 1) % h, j)) not in east and c not in state.south
        else (i, j)
        for i, j in state.south
    )
    return State(width=w, height=h, east=east, south=south)


def find_stop(state: State) -> int:
    prev: State | None = None
    for i in count(1):
        state = step(state)
        if state == prev:
            return i
        prev = state
    return 0


def solve() -> tuple[int, int]:
    state = parse(read_puzzle())
    return find_stop(state), 0


if __name__ == '__main__':
    print(solve())
