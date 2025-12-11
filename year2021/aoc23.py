# https://adventofcode.com/2021/day/23
# tags: $graph-traversal #dijkstra

import math
import re
from collections import defaultdict
from heapq import heappop, heappush
from itertools import count

from utils_proxy import read_puzzle

type Spot = str | None
type Spots = tuple[Spot, ...]
type Room = tuple[str, ...]
type Rooms = tuple[Room, ...]

ROOM_POS = (2, 4, 6, 8)
SPOT_POS = (0, 1, 3, 5, 7, 9, 10)
AMPHS = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
STEP_COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def parse(s: str) -> Rooms:
    amphipods: list[str] = re.findall(r'[A-D]', s)
    return tuple((amphipods[i], amphipods[i + 4]) for i in range(4))


def is_reachable(spots: Spots, spot_idx: int, room_idx: int) -> bool:
    a, b = ROOM_POS[room_idx], SPOT_POS[spot_idx]
    from_, to = min(a, b), max(a, b)
    return all(spots[i] is None for i in range(7) if from_ < SPOT_POS[i] < to)


def min_energy_to_organize(rooms: Rooms) -> int:  # noqa: C901
    counter = count(1)
    queue: list[tuple[int, int, Spots, Rooms]] = [(0, 0, (None,) * 7, rooms)]
    costs = defaultdict[tuple[Spots, Rooms], float](lambda: math.inf)
    r_size = len(rooms[0])
    target = tuple((amph,) * r_size for amph in AMPHS)
    while True:
        energy, _, spots, rooms = heappop(queue)
        if rooms == target:
            return energy
        candidates = list[tuple[int, Spots, Rooms]]()
        for i, spot in enumerate(spots):
            if spot is None:
                continue
            spots_2 = (*spots[:i], None, *spots[i + 1 :])
            for j, room in enumerate(rooms):
                if (
                    len(room) == r_size
                    or AMPHS[spot] != j
                    or not all(AMPHS[r] == j for r in room)
                    or not is_reachable(spots, i, j)
                ):
                    continue
                steps = abs(SPOT_POS[i] - ROOM_POS[j]) + r_size - len(room)
                energy_2 = energy + STEP_COSTS[spot] * steps
                rooms_2 = (*rooms[:j], (spot, *room), *rooms[j + 1 :])
                candidates.append((energy_2, spots_2, rooms_2))
        for j, room in enumerate(rooms):
            if len(room) == 0 or all(AMPHS[r] == j for r in room):
                continue
            rooms_2 = (*rooms[:j], room[1:], *rooms[j + 1 :])
            for i, spot in enumerate(spots):
                if spot is not None or not is_reachable(spots, i, j):
                    continue
                steps = abs(SPOT_POS[i] - ROOM_POS[j]) + r_size - len(room) + 1
                energy_2 = energy + STEP_COSTS[room[0]] * steps
                spots_2 = (*spots[:i], room[0], *spots[i + 1 :])
                candidates.append((energy_2, spots_2, rooms_2))
        for energy_2, spots_2, rooms_2 in candidates:
            if energy_2 < costs[spots_2, rooms_2]:
                costs[spots_2, rooms_2] = energy_2
                heappush(queue, (energy_2, next(counter), spots_2, rooms_2))


def expand(rooms: Rooms) -> Rooms:
    extras = (('D', 'D'), ('C', 'B'), ('B', 'A'), ('A', 'C'))
    return tuple((r[0], *extra, r[1]) for extra, r in zip(extras, rooms))


def solve() -> tuple[int, int]:
    rooms = parse(read_puzzle())
    return min_energy_to_organize(rooms), min_energy_to_organize(expand(rooms))


if __name__ == '__main__':
    print(solve())
