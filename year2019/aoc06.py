from networkx import Graph

from helpers import read_puzzle
import networkx as nx

MapData = list[tuple[str, ...]]
Node = tuple[str, int]


def parse(s: str) -> MapData:
    return [tuple(line.split(')')) for line in s.split()]


def count_orbits(g: Graph) -> int:
    return sum(nx.shortest_path_length(g, x, 'COM') for x in g.nodes)


def count_min_transfers(g: Graph) -> int:
    return nx.shortest_path_length(g, 'YOU', 'SAN') - 2


def solve() -> tuple[int, int]:
    g = nx.Graph(parse(read_puzzle()))
    return count_orbits(g), count_min_transfers(g)


if __name__ == '__main__':
    print(solve())
