from collections import deque
from dataclasses import dataclass, replace
from itertools import chain
from typing import Dict, List, Optional, Tuple

from helpers import read_puzzle

Square = Tuple[int, int]
Squares = Dict[Square, str]


@dataclass(order=True)
class Unit:
    sq: Square
    type: str
    hp: int = 200
    power: int = 3

    def __str__(self):
        return type

    def is_enemy(self, target: 'Unit'):
        return self.type != target.type

    def is_in_range(self, target: 'Unit'):
        si, sj = self.sq
        ti, tj = target.sq
        return ((si == ti and abs(sj - tj) == 1) or
                (sj == tj and abs(si - ti) == 1))


@dataclass
class State:
    height: int
    width: int
    map: Squares
    units: List[Unit]
    rounds_played: int = 0
    finished: bool = False

    @classmethod
    def fromstring(cls, s: str):
        lines = s.splitlines()
        map_, units = {}, []
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                map_[(i, j)] = ch
                if ch in 'EG':
                    units.append(Unit((i, j), ch))
        return cls(height=len(lines), width=len(lines[0]),
                   map=map_, units=units)

    def __str__(self, hp: bool = False):
        """Get a text representation of the map."""
        map_ = [''.join(self.map[(i, j)] for j in range(self.width))
                for i in range(self.height)]
        if hp:
            for unit in sorted(self.units):
                i, j = unit.sq
                map_[i] += ', ' if len(map_[i]) > self.width else '   '
                map_[i] += f'{unit.type}({unit.hp})'
        return '\n'.join(map_)

    def deepcopy(self) -> 'State':
        """Return a deep copy of the state."""
        return replace(self, map=self.map.copy(),
                       units=[replace(u) for u in self.units])

    def squares_in_range(self, sq: Square) -> List[Square]:
        """Get all open (.) squares adjacent to the square."""
        i, j = sq
        return [sq2 for sq2 in [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)]
                if self.map.get(sq2, None) == '.']

    def find_path(self, unit: Unit, sq_trg: Square) -> \
            Optional[Tuple[int, Square, Square]]:
        """Find a square along the shortest path from the unit
        to the target square and the path's length."""
        # Temporarily hide the source unit so that BFS can work
        self.map[unit.sq] = '.'
        # Breadth-first search (starting from the end)
        dist = {sq_trg: 0}
        queue = deque([sq_trg])
        while queue:
            sq = queue.popleft()
            if sq == unit.sq:
                break
            for sq_next in self.squares_in_range(sq):
                if sq_next not in dist:
                    dist[sq_next] = dist[sq] + 1
                    queue.append(sq_next)
        else:  # no break
            self.map[unit.sq] = unit.type
            return None
        # If there are multiple steps from the start along the shortest path
        # available, choose in reading order.
        sqs = sorted((dist[sq], sq_trg, sq)
                     for sq in self.squares_in_range(unit.sq)
                     if sq in dist)
        self.map[unit.sq] = unit.type
        return sqs[0]

    def move(self, unit, targets: List[Unit]):
        sqs = set(chain(*(self.squares_in_range(t.sq) for t in targets)))
        reachable = sorted(p for sq in sqs
                           if (p := self.find_path(unit, sq)) is not None)
        if not reachable:
            return
        self.map[unit.sq] = '.'
        unit.sq = reachable[0][2]
        self.map[unit.sq] = unit.type

    def hit(self, target: Unit, dmg: int):
        target.hp -= min(dmg, target.hp)
        if target.hp <= 0:
            self.units.remove(target)
            self.map[target.sq] = '.'

    def hash(self) -> int:
        return self.rounds_played * sum(u.hp for u in self.units)


def play_round(st: State) -> State:
    """Simulate one round of the game without mutating the state."""
    st = st.deepcopy()
    # Units take turns in reading order of their stating positions
    st.units.sort()
    for unit in st.units.copy():  # st.units is mutated when a unit dies
        if unit.hp <= 0:
            continue

        targets = sorted(filter(unit.is_enemy, st.units))
        if not targets:
            st.finished = True
            break

        targets_in_range = list(filter(unit.is_in_range, targets))
        if not targets_in_range:
            st.move(unit, targets)

        # Check adjacent targets again after moving
        targets_in_range = list(filter(unit.is_in_range, targets))
        if not targets_in_range:
            continue

        # Target a unit with the lowest hp in reading order
        targets_in_range.sort(key=lambda t: (t.hp, t.sq))
        st.hit(targets_in_range[0], dmg=unit.power)
    else:  # no break, i.e. the combat has not ended
        st.rounds_played += 1

    return st


def outcome(s: str) -> int:
    st = State.fromstring(s)
    while not st.finished:
        st = play_round(st)
    return st.hash()


def solve():
    return outcome(read_puzzle())


if __name__ == '__main__':
    print(solve())
