# https://adventofcode.com/2018/day/8

from collections.abc import Iterable
from dataclasses import dataclass, field

from helpers import read_puzzle


@dataclass
class Node:
    end: int | None = None
    children: list['Node'] = field(default_factory=list)
    meta: list[int] = field(default_factory=list)


def parse_tree(s: str):
    def parse_node(start: int):
        n_children, n_meta = nums[start : start + 2]
        root = Node()
        start += 2
        for _ in range(n_children):
            child = parse_node(start)
            root.children.append(child)
            start = child.end + 1  # type: ignore
        root.end = start + n_meta - 1
        root.meta = nums[start : root.end + 1]
        return root

    nums = [int(n) for n in s.split()]
    return parse_node(0)


def metadata_rec(node: Node) -> Iterable[int]:
    for child in node.children:
        yield from metadata_rec(child)
    yield from node.meta


def metadata_as_indices(node: Node) -> int:
    children = (
        node.children[i - 1] for i in node.meta if 0 < i <= len(node.children)
    )
    return sum(
        node.meta if not node.children else map(metadata_as_indices, children)
    )


def solve():
    tree = parse_tree(read_puzzle())
    return sum(metadata_rec(tree)), metadata_as_indices(tree)


if __name__ == '__main__':
    print(solve())
