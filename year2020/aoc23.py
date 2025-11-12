# https://adventofcode.com/2020/day/23


from itertools import pairwise
from typing import TYPE_CHECKING

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterator


type Links = list[int]


def parse(s: str) -> Links:
    """Get a list of connections. If 1 is followed by 2, then links[1] == 2.

    The first element in the list is the starting cup.
    """
    links = [0 for _ in range(len(s) + 1)]
    for a, b in pairwise(s + s[0]):
        links[int(a)] = int(b)
    links[0] = int(s[0])
    return links


def walk(links: Links, start: int | None = None) -> Iterator[int]:
    if start is None:
        start = links[0]
    node = start
    while True:
        yield node
        node = links[node]
        if node == start:
            break


def to_str(links: Links, start: int | None = None) -> str:
    return ' '.join(str(n) for n in walk(links, start))


def simulate(links: Links, steps: int) -> Links:
    min_, max_ = 1, len(links) - 1
    cur = links[0]
    for _ in range(steps):
        n3 = links[n2 := links[n1 := links[cur]]]
        links[cur] = links[n3]

        dest = cur
        while True:
            dest = dest - 1 if dest > min_ else max_
            if dest != n1 and dest != n2 and dest != n3:  # noqa: PLR1714
                break

        links[n3] = links[dest]
        links[dest] = n1
        cur = links[cur]
    links[0] = cur
    return links


def pad(links: Links, total: int) -> Links:
    max_ = len(links) - 1
    links += [0] * (total - max_)
    *_, last = walk(links)
    for val in range(max_ + 1, total + 1):
        links[last] = last = val
    links[last] = links[0]
    return links


def part1(links: Links) -> str:
    links = simulate(links, steps=100)
    return to_str(links, start=1)[1:].replace(' ', '')


def part2(links: Links) -> int:
    links = simulate(pad(links, total=1_000_000), steps=10_000_000)
    return links[1] * links[links[1]]


def solve() -> tuple[str, int]:
    cups = read_puzzle()
    return part1(parse(cups)), part2(parse(cups))


if __name__ == '__main__':
    print(solve())
