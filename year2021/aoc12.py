# https://adventofcode.com/2021/day/12
# tags: #graph-traversal #paths #recursion

# ruff: noqa: FBT001 FBT003

import re
from collections import defaultdict
from functools import cache
from itertools import batched

from helpers import read_puzzle

type Graph = defaultdict[str, set[str]]  # adjacency set


def parse(s: str) -> Graph:
    g: Graph = defaultdict(set)
    for a, b in batched(re.findall(r'\w+', s), 2, strict=True):
        g[a].add(b)
        g[b].add(a)
    return g


def count_all_paths(g: Graph, *, allow_return: bool = False) -> int:
    @cache
    def paths(node: str, visited: frozenset[str], has_return: bool) -> int:
        if node == 'end':
            return 1
        if node in visited:
            if not allow_return or has_return or node == 'start':
                return 0
            has_return = True
        if node in small or node == 'start':
            visited |= {node}
        return sum(paths(n, visited, has_return) for n in g[node])

    small = {c for c in g if c.islower()} - {'start', 'end'}
    return paths('start', frozenset[str](), False)


def solve() -> tuple[int, int]:
    g = parse(read_puzzle())
    return count_all_paths(g), count_all_paths(g, allow_return=True)


if __name__ == '__main__':
    print(solve())
