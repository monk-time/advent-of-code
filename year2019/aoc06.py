from helpers import read_puzzle

MapData = list[tuple[str, ...]]
Node = tuple[str, int]


def parse(s: str) -> MapData:
    return [tuple(line.split(')')) for line in s.split()]


def create_world_structure(m: MapData):
    children, parents = {}, {}
    for parent, child in m:
        if parent not in children:
            children[parent] = {child}
        else:
            children[parent].add(child)
        if child not in parents:
            parents[child] = parent
    return children, parents


def count_orbits(m: MapData) -> int:
    children, parents = create_world_structure(m)
    count, depth = 0, 0
    planets = {'COM'}
    while True:
        next_planets = []
        depth += 1
        for planet in planets:
            pl_children = children.get(planet, set())
            if not pl_children:
                continue
            count += len(pl_children) * depth
            next_planets += list(pl_children)
        if not next_planets:
            return count
        planets = next_planets


def count_min_transfers(m: MapData) -> int:
    children, parents = create_world_structure(m)
    depth = 0
    planets = {'YOU'}
    visited = set()
    while True:
        next_planets = set()
        depth += 1
        for planet in planets:
            visited.add(planet)
            pl_children = children.get(planet, set())
            pl_parent = parents.get(planet, None)
            next_planets |= (pl_children | {pl_parent}) - visited
        if 'SAN' in next_planets:
            return depth - 2  # not counting first moves from YOU and SAN
        planets = next_planets


def solve() -> tuple[int, int]:
    puzzle = parse(read_puzzle())
    return count_orbits(puzzle), count_min_transfers(puzzle)


if __name__ == '__main__':
    print(solve())
