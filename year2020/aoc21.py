# https://adventofcode.com/2020/day/21

from __future__ import annotations

import re
from collections import defaultdict, deque
from typing import TYPE_CHECKING, NewType, TypedDict

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterable

Ingr = NewType('Ingr', str)
Alrg = NewType('Alrg', str)
type AlrgMap = dict[Alrg, Ingr]


class Food(TypedDict):
    ingredients: set[Ingr]
    allergens: set[Alrg]


def parse(s: str) -> Iterable[Food]:
    lines = s.splitlines()
    for line in lines:
        words = re.findall(r'\w+', line)
        i = words.index('contains')
        yield {'ingredients': set(words[:i]), 'allergens': set(words[i + 1 :])}


def find_allergens(foods: Iterable[Food]) -> AlrgMap:
    all_alrgs = set[Alrg]().union(*(f['allergens'] for f in foods))
    all_ingrs = set[Ingr]().union(*(f['ingredients'] for f in foods))
    suspects: defaultdict[Alrg, set[Ingr]] = defaultdict(all_ingrs.copy)
    for food in foods:
        for alrg in food['allergens']:
            suspects[alrg] &= food['ingredients']
    solved = set[Ingr]()
    queue = deque(all_alrgs)
    while queue:
        alrg = queue.popleft()
        suspects[alrg] -= solved
        if len(suspects[alrg]) == 1:
            solved.add(next(iter(suspects[alrg])))
        else:
            queue.append(alrg)
    return {k: next(iter(v)) for k, v in suspects.items()}


def count_safe(foods: Iterable[Food], alrg_map: AlrgMap) -> int:
    all_ingrs = set[Ingr]().union(*(f['ingredients'] for f in foods))
    safe_ingrs = all_ingrs - set(alrg_map.values())
    return sum(len(f['ingredients'] & safe_ingrs) for f in foods)


def format_bad_ingrs(alrg_map: AlrgMap) -> str:
    return ','.join(alrg_map[alrg] for alrg in sorted(alrg_map.keys()))


def solve() -> tuple[int, str]:
    foods = list(parse(read_puzzle()))
    alrg_map = find_allergens(foods)
    return (count_safe(foods, alrg_map), format_bad_ingrs(alrg_map))


if __name__ == '__main__':
    print(solve())
