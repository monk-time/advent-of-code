from math import inf

from helpers import read_puzzle

Wire = list[tuple[str, int]]
Coord = tuple[int, int]


def parse(s: str) -> tuple[Wire, Wire]:
    wire1, wire2 = s.split()
    parse_wire = lambda s_: [(move[0], int(move[1:])) for move in s_.split(',')]
    return parse_wire(wire1), parse_wire(wire2)


step_by_dir = {
    'U': (0, 1),
    'D': (0, -1),
    'R': (1, 0),
    'L': (-1, 0),
}


def trace_wire(wire: Wire) -> set[Coord]:
    cursor = (0, 0)
    mem = {cursor}
    for dir_, steps in wire:
        dx, dy = step_by_dir[dir_]
        for _ in range(steps):
            cursor = (cursor[0] + dx, cursor[1] + dy)
            mem.add(cursor)
    return mem


def find_closest_intersection(wire1: Wire, wire2: Wire) -> int:
    mem1 = trace_wire(wire1)
    mem2 = trace_wire(wire2)
    intersections = mem1 & mem2
    closest = (inf, inf)
    manhattan = lambda c: abs(c[0]) + abs(c[1])
    for coord in intersections:
        if 0 < manhattan(coord) < manhattan(closest):
            closest = coord
    return manhattan(closest)


def solve() -> tuple[int, int]:
    wire1, wire2 = parse(read_puzzle())
    part1 = find_closest_intersection(wire1, wire2)
    return part1, 0


if __name__ == '__main__':
    print(solve())
