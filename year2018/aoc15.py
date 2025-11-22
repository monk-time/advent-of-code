# https://adventofcode.com/2018/day/15

from dataclasses import dataclass, replace

from utils_proxy import read_puzzle

Square = tuple[int, int]


def around(sq: Square) -> tuple[Square, Square, Square, Square]:
    i, j = sq
    return ((i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j))


@dataclass(order=True)
class Unit:
    sq: Square
    type: str
    hp: int = 200
    power: int = 3

    def __str__(self):
        return self.type

    def is_enemy(self, target: Unit):
        return self.type != target.type


@dataclass
class State:
    height: int
    width: int
    map: dict[Square, Unit | str]
    units: list[Unit]
    rounds_played: int = 0
    finished: bool = False

    @classmethod
    def fromstring(cls, s: str, elf_power: int = 3):
        lines = s.splitlines()
        map_: dict[Square, Unit | str] = {}
        units: list[Unit] = []
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                if ch in 'EG':
                    power = elf_power if ch == 'E' else 3
                    unit = Unit((i, j), ch, power=power)
                    units.append(unit)
                    map_[i, j] = unit
                else:
                    map_[i, j] = ch
        return cls(
            height=len(lines), width=len(lines[0]), map=map_, units=units
        )

    def __str__(self, *, hp: bool = False):
        """Get a text representation of the map."""
        map_ = [
            ''.join(str(self.map[i, j]) for j in range(self.width))
            for i in range(self.height)
        ]
        if hp:
            for unit in sorted(self.units):
                i, _ = unit.sq
                map_[i] += ', ' if len(map_[i]) > self.width else '   '
                map_[i] += f'{unit.type}({unit.hp})'
        return '\n'.join(map_)

    def deepcopy(self) -> State:
        """Return a deep copy of the state."""
        units_new: list[Unit] = []
        map_new = self.map.copy()
        for unit in self.units:
            unit_new = replace(unit)
            units_new.append(unit_new)
            map_new[unit_new.sq] = unit_new
        return replace(self, map=map_new, units=units_new)

    def targets_in_range(self, u: Unit) -> list[Unit]:
        """Get all enemies adjacent to the unit."""
        return [
            t
            for sq2 in around(u.sq)
            if (t := self.map.get(sq2, None))
            and isinstance(t, Unit)
            and u.is_enemy(t)
        ]

    def find_path(self, unit: Unit) -> Square | None:
        """Find the next step needed to reach the closest enemy.

        If multiple enemy are at the same distance, the one which is first
        in reading order is chosen. If multiple steps (ULRD) would put the
        unit equally closer to the target, again the reading order is used.

        Uses breadth-first search, modified to visit all nodes at the same
        distance from the start, and to label each with the 'sector' it
        belongs to based on the direction of the first step, resolving ties
        in reading order.
        """
        # Each visited square is labeled with the direction of the first step
        # that would bring the unit to it.
        # ULRD -> 0123
        visited = dict(zip((*around(unit.sq), unit.sq), range(5)))
        # Points are always added to layer in the order of their labels
        layer: list[Square] = [unit.sq]
        final_layer = False
        nearest_in_range: list[Square] = []
        while layer and not final_layer:
            next_layer: list[Square] = []
            for sq in layer:
                for sq_next in around(sq):
                    x = self.map.get(sq_next, None)
                    if x is None or x == '#':
                        continue
                    if isinstance(x, Unit):
                        if unit.is_enemy(x):
                            final_layer = True
                            nearest_in_range.append(sq)
                        continue
                    # The initial step has to be special-cased
                    if sq_next not in visited or sq is unit.sq:
                        next_layer.append(sq_next)
                        if sq is not unit.sq:
                            visited[sq_next] = visited[sq]
            layer = next_layer
        if not final_layer:
            return None
        chosen_in_range = min(nearest_in_range)
        direction = visited[chosen_in_range]
        return around(unit.sq)[direction]

    def move(self, unit: Unit):
        if not (sq_new := self.find_path(unit)):
            return
        self.map[unit.sq] = '.'
        unit.sq = sq_new
        self.map[unit.sq] = unit

    def hit(self, target: Unit, dmg: int):
        target.hp -= min(dmg, target.hp)
        if target.hp <= 0:
            self.units.remove(target)
            self.map[target.sq] = '.'

    def hash(self) -> int:
        return self.rounds_played * sum(u.hp for u in self.units)

    def elfs_alive(self) -> int:
        return len([u for u in self.units if u.type == 'E'])


def play_round(st: State) -> State:
    """Simulate one round of the game without mutating the state."""
    st = st.deepcopy()
    # Units take turns in reading order of their stating positions
    st.units.sort()
    for unit in st.units.copy():  # st.units is mutated when a unit dies
        if unit.hp <= 0:
            continue

        if not next(filter(unit.is_enemy, st.units), None):
            st.finished = True
            break

        targets_in_range = st.targets_in_range(unit)
        if not targets_in_range:
            st.move(unit)
            targets_in_range = st.targets_in_range(unit)
            # Check adjacent targets again after moving
            if not targets_in_range:
                continue

        # Target a unit with the lowest hp in reading order
        targets_in_range.sort(key=lambda t: (t.hp, t.sq))
        st.hit(targets_in_range[0], dmg=unit.power)
    else:  # no break, i.e. the combat has not ended
        st.rounds_played += 1

    return st


def outcome(s: str, *, force_elf_victory: bool = False) -> int:
    elf_power = 3
    st = State.fromstring(s, elf_power=elf_power)
    elfs_at_start = st.elfs_alive()
    while not st.finished:
        st = play_round(st)
    if force_elf_victory:
        while st.elfs_alive() != elfs_at_start:
            elf_power += 1
            st = State.fromstring(s, elf_power=elf_power)
            while not st.finished:
                st = play_round(st)

    return st.hash()


def solve():
    puzzle = read_puzzle()
    return outcome(puzzle), outcome(puzzle, force_elf_victory=True)


if __name__ == '__main__':
    print(solve())
