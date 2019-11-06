from dataclasses import dataclass
from itertools import chain
from typing import Dict, List, Tuple

from helpers import block_unwrap, read_puzzle

Square = Tuple[int, int]
Squares = Dict[Square, str]


# TODO: remove or integrate into __str__
def replace_chars(s: str, chars: Squares):
    """Replace characters in a multiline string by a coords-to-char mapping."""
    lines = s.splitlines()
    for sq, ch in chars.items():
        i, j = sq
        lines[i] = lines[i][:j] + ch + lines[i][j + 1:]
    return '\n'.join(lines)


class State:
    def __init__(self, s: str):
        super().__init__()
        lines = s.splitlines()
        self.height: int = len(lines)
        self.width: int = len(lines[0])
        self.map: Squares = {}
        self.units: List[Unit] = []
        self.rounds_played: int = 0
        self.finished: bool = False
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                self.map[(i, j)] = ch
                if ch in 'EG':
                    self.units.append(Unit((i, j), ch))

    def __str__(self, hp: bool = False):
        """Get a text representation of the map."""
        map_ = [''.join(self.map[(i, j)] for j in range(self.width))
                for i in range(self.height)]
        if hp:
            for unit in self.units:
                i, j = unit.sq
                map_[i] += ', ' if len(map_[i]) > self.width else '   '
                map_[i] += f'{unit.type}({unit.hp})'
        return '\n'.join(map_)

    def squares_in_range(self, sq: Square) -> List[Square]:
        """Get all open (.) squares adjacent to the square."""
        i, j = sq
        return [sq2 for sq2 in [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)]
                if self.map.get(sq2, None) == '.']


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


def play_round(st: State):
    # Units take turns in reading order of their stating positions
    st.units.sort()
    for unit in st.units.copy():
        if unit.hp <= 0:
            continue

        targets = sorted(filter(unit.is_enemy, st.units))
        if not targets:
            st.finished = True
            return

        targets_in_range = list(filter(unit.is_in_range, targets))
        if not targets_in_range:
            # TODO: move
            sqs = set(chain(*(st.squares_in_range(t.sq) for t in targets)))
            # if none available, finish
            # find the closest open square (if several, choose in RO)
            # move
            pass

        # Check adjacent targets again after moving
        targets_in_range = list(filter(unit.is_in_range, targets))
        if not targets_in_range:
            continue
        # Target a unit with the lowest hp in reading order
        targets_in_range.sort(key=lambda t: (t.hp, t.sq))
        target = targets_in_range[0]
        target.hp -= unit.power
        if target.hp <= 0:
            st.units.remove(target)
            st.map[target.sq] = '.'

    st.rounds_played += 1


def solve():
    return State(read_puzzle())


if __name__ == '__main__':
    # print(solve())
    # st_ = State(read_puzzle())
    st_ = State(block_unwrap("""
        #######
        #E..G.#
        #...#.#
        #.G.#G#
        #######
    """, border=False))
    print('\n' * 20)
    while True:
        print(f'After {st_.rounds_played} rounds:')
        print(st_.__str__(hp=True))
        input()
        play_round(st_)
