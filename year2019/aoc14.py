import math
import re
from dataclasses import dataclass
from pprint import pprint

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


def calc_ore_for_fuel(reactions: Reactions) -> int:
    edges = {r.name: list(r.inputs) for r in reactions.values()}
    vertices_sorted = nx.topological_sort(nx.DiGraph(edges))
    queue = {v: 0 for v in reversed(list(vertices_sorted))}
    queue['FUEL'] = 1
    while len(queue) > 1:
        name, target_amount = queue.popitem()
        reaction = reactions[name]
        repeat_times = math.ceil(target_amount / reaction.amount)
        for input_name, input_amount in reaction.inputs.items():
            total = repeat_times * input_amount
            queue[input_name] += total
    return queue['ORE']


def solve() -> tuple[int, int]:
    reactions = parse(read_puzzle())
    pprint(reactions)
    part1 = calc_ore_for_fuel(reactions)
    return part1, 0


if __name__ == '__main__':
    print(solve())
