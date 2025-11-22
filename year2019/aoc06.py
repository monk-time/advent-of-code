# https://adventofcode.com/2019/day/6

import networkx as nx

from utils_proxy import read_puzzle

MapData = list[tuple[str, ...]]
Node = tuple[str, int]


def parse(s: str) -> MapData:
    return [tuple(line.split(')')) for line in s.split()]


def count_orbits(g: nx.Graph[str]) -> int:
    return int(sum(nx.shortest_path_length(g, x, 'COM') for x in g.nodes))


def count_min_transfers(g: nx.Graph[str]) -> int:
    return int(nx.shortest_path_length(g, 'YOU', 'SAN')) - 2


def solve() -> tuple[int, int]:
    g: nx.Graph[str] = nx.Graph(parse(read_puzzle()))
    return count_orbits(g), count_min_transfers(g)


if __name__ == '__main__':
    print(solve())
