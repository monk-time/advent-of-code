# https://adventofcode.com/2020/day/23


from itertools import pairwise
from typing import TYPE_CHECKING

from helpers import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Iterator


class Node[T]:
    __slots__ = ('next', 'val')

    def __init__(self, val: T, next: Node[T] | None = None):  # noqa: A002
        self.val = val
        self.next = next or self

    def __repr__(self) -> str:
        return f'Node({self.val}, {self.next.val})'

    def walk(self) -> Iterator[Node[T]]:
        node = self
        while True:
            yield node
            node = node.next
            if node == self:
                break

    def to_str(self) -> str:
        return ' '.join(str(n.val) for n in self.walk())


def parse(s: str) -> Node[int]:
    nodes = [Node(val=int(val)) for val in s]
    for n1, n2 in pairwise([*nodes, nodes[0]]):
        n1.next = n2
    return nodes[0]


def simulate(node: Node[int], steps: int) -> Node[int]:
    nodes = {n.val: n for n in node.walk()}
    min_, max_ = min(nodes), max(nodes)
    for _ in range(steps):
        n3 = (n2 := (n1 := node.next).next).next
        node.next = n3.next

        val = node.val
        while True:
            val = val - 1 if val > min_ else max_
            if val != n1.val and val != n2.val and val != n3.val:  # noqa: PLR1714
                break
        dest = nodes[val]

        n3.next = dest.next
        dest.next = n1
        node = node.next
    return nodes[1]


def pad(node: Node[int], total: int) -> Node[int]:
    max_val = max(n.val for n in node.walk())
    *_, last = node.walk()
    new_node = node
    for val in range(total, max_val, -1):
        new_node = Node(val, new_node)
    last.next = new_node
    return node


def part1(node: Node[int]) -> str:
    return simulate(node, steps=100).to_str()[1:].replace(' ', '')


def part2(node: Node[int]) -> int:
    node = simulate(pad(node, total=1_000_000), steps=10_000_000)
    return node.next.val * node.next.next.val


def solve() -> tuple[str, int]:
    cups = read_puzzle()
    return part1(parse(cups)), part2(parse(cups))


if __name__ == '__main__':
    print(solve())
