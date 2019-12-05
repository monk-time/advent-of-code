import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Match, Optional, Tuple

from helpers import read_puzzle


@dataclass
class Group:
    id_: int
    team: str
    units: int
    unit_hp: int
    weak: List[str]
    immune: List[str]
    dmg: int
    dmg_type: str
    init: int
    boost: int = 0

    @classmethod
    def frommatch(cls, m: Match, **kwargs) -> 'Group':
        d = {k: int(v) if v and v.isdigit() else v
             for k, v in m.groupdict().items()}
        traits = parse_traits(d['traits'])
        del d['traits']
        return Group(**d, **kwargs, **traits)

    def __hash__(self):
        return hash(self.name)

    @property
    def name(self) -> str:
        return f'{self.team} group {self.id_}'

    @property
    def power(self) -> int:
        return self.units * (self.dmg + self.boost)

    def dmg_to(self, target: 'Group') -> int:
        if self.dmg_type in target.immune:
            return 0
        return self.power * (2 if self.dmg_type in target.weak else 1)


def parse(s: str) -> Tuple[List[Group], List[Group]]:
    regex = r"""^
        (?P<units>\d+)\ units.+?
        (?P<unit_hp>\d+)\ hit\ points\ 
        (?:\((?P<traits>.+?)\))?.+?
        (?P<dmg>\d+)\ (?P<dmg_type>\w+?)\ damage.+?
        (?P<init>\d+)
        $"""
    flags = re.MULTILINE | re.VERBOSE
    immune, infect = (
        [Group.frommatch(m, id_=i, team=['Immune System', 'Infection'][j])
         for i, m in enumerate(re.finditer(regex, s2, flags), start=1)]
        for j, s2 in enumerate(s.split('\n\n')))
    return immune, infect


def parse_traits(s: str) -> Dict[str, List[str]]:
    d = {'weak': [], 'immune': []}
    if s:
        for s2 in s.split('; '):
            trait, dmg_types = s2.split(' to ')
            d[trait] = dmg_types.split(', ')
    return d


def fight(immune: List[Group], infect: List[Group]):
    teams = {'Immune System': immune, 'Infection': infect}
    enemy_teams = {'Immune System': infect, 'Infection': immune}
    targets = {}

    # Target selection phase
    for team_name, team in teams.items():
        enemy_team = enemy_teams[team_name]
        for g in sorted(team, key=lambda x: (-x.power, -x.init)):
            ts = sorted((x for x in enemy_team if x not in targets.values()),
                        key=lambda x: (-g.dmg_to(x), -x.power, -x.init))
            if ts and g.dmg_to(ts[0]) > 0:
                targets[g] = ts[0]

    # Attacking phase
    is_stalemate = True
    for g in sorted((*immune, *infect), key=lambda x: -x.init):
        if g not in targets or g.units == 0:
            continue
        t = targets[g]
        units_killed = g.dmg_to(t) // t.unit_hp
        is_stalemate &= units_killed == 0
        t.units = max(0, t.units - units_killed)
        if t.units == 0:
            teams[t.team].remove(t)
    return immune, infect, is_stalemate


def combat(immune: List[Group], infect: List[Group]) -> Optional[int]:
    while immune and infect:
        immune, infect, is_stalemate = fight(immune, infect)
        if is_stalemate:
            return None
    return sum(g.units for g in (*immune, *infect))


def min_boost(immune: List[Group], infect: List[Group]) -> int:
    boost = 0
    while True:
        immune2, infect2 = deepcopy(immune), deepcopy(infect)
        for g in immune2:
            g.boost = boost
        result = combat(immune2, infect2)
        if result and immune2:
            break
        boost += 1
    return result


def solve():
    puzzle = read_puzzle()
    return combat(*parse(puzzle)), min_boost(*parse(puzzle))


if __name__ == '__main__':
    print(solve())
