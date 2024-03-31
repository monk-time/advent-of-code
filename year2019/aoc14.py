# https://adventofcode.com/2019/day/14

import math
import re
from dataclasses import dataclass

import networkx as nx

from helpers import read_puzzle


@dataclass
class Reaction:
    inputs: dict[str, int]
    amount: int
    name: str


Reactions = dict[str, Reaction]


def parse_reaction(s: str) -> Reaction:
    matches = re.findall(r'(\d+) ([A-Z]+)', s)
    amount = int(matches[-1][0])
    name = matches[-1][1]
    inputs = {m[1]: int(m[0]) for m in matches[:-1]}
    return Reaction(amount=amount, name=name, inputs=inputs)


def parse(s: str) -> Reactions:
    return {(r := parse_reaction(line)).name: r for line in s.split('\n')}


def calc_ore_for_fuel(reactions: Reactions, fuel: int = 1) -> tuple[int, int]:
    edges = {r.name: list(r.inputs) for r in reactions.values()}
    vertices_sorted = nx.topological_sort(nx.DiGraph(edges))
    queue = dict.fromkeys(reversed(list(vertices_sorted)), 0)
    queue['FUEL'] = fuel
    coef = 1
    while len(queue) > 1:
        name, target_amount = queue.popitem()
        reaction = reactions[name]
        if target_amount % reaction.amount:
            local_coef = reaction.amount * (
                target_amount // math.gcd(target_amount, reaction.amount)
            )
            coef *= local_coef // math.gcd(local_coef, coef)
        repeat_times = math.ceil(target_amount / reaction.amount)
        for input_name, input_amount in reaction.inputs.items():
            queue[input_name] += repeat_times * input_amount
    return queue['ORE'], coef


def calc_fuel_from_trillion_ore(reactions: Reactions) -> int:
    ore_per_fuel, coef = calc_ore_for_fuel(reactions)
    flawless_fuel = coef
    ore_per_flawless_fuel, _ = calc_ore_for_fuel(reactions, fuel=flawless_fuel)
    flawless_times = 1_000_000_000_000 // ore_per_flawless_fuel
    fuel = flawless_fuel * flawless_times
    ore_left = 1_000_000_000_000 % ore_per_flawless_fuel

    extra_fuel, extra_ore, next_fuel = 0, 0, 0
    while extra_ore <= ore_left:
        next_fuel = (ore_left - extra_ore) // ore_per_fuel or 1
        extra_fuel += next_fuel
        extra_ore = calc_ore_for_fuel(reactions, extra_fuel)[0]
    return fuel + extra_fuel - next_fuel


def solve() -> tuple[int, int]:
    reactions = parse(read_puzzle())
    part1, _ = calc_ore_for_fuel(reactions)
    return part1, calc_fuel_from_trillion_ore(reactions)


if __name__ == '__main__':
    print(solve())
