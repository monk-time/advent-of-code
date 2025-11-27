# https://adventofcode.com/2021/day/18
# tags: #trees

import functools
from collections.abc import Generator
from dataclasses import dataclass, field
from itertools import permutations
from math import ceil
from typing import TYPE_CHECKING, Any, Literal

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable


@dataclass(slots=True)
class Node:
    left: TreeNode
    right: TreeNode
    parent: Node | None = field(repr=False, default=None)

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)

    def __str__(self) -> str:
        return f'[{self.left},{self.right}]'

    def __repr__(self) -> str:
        return str(self)


@dataclass(slots=True)
class Leaf:
    value: int
    parent: Node | None = field(repr=False, default=None)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


type TreeNode = Node | Leaf
type TreeNodeN = tuple[TreeNode, int]


def parse_tree(s: str) -> Node:
    stack = list[TreeNode]()
    for ch in s:
        if ch.isdigit():
            stack.append(Leaf(int(ch)))
        elif ch == ']':
            right, left = stack.pop(), stack.pop()
            parent = Node(left=left, right=right)
            left.parent = right.parent = parent
            stack.append(parent)
    assert isinstance(stack[0], Node)
    return stack[0]


def parse(s: str) -> tuple[Node, ...]:
    return tuple(parse_tree(line) for line in s.splitlines())


def inorder_walk(node: TreeNode) -> Generator[TreeNodeN]:
    def rec(node: TreeNode, depth: int = 0) -> Generator[TreeNodeN]:
        if isinstance(node, Node):
            yield from rec(node.left, depth + 1)
        yield node, depth
        if isinstance(node, Node):
            yield from rec(node.right, depth + 1)

    yield from rec(node)


def inorder_near(leaf: Leaf, dir_: Literal['left', 'right']) -> Leaf | None:
    node = leaf
    while node.parent and node.parent[dir_] is node:
        node = node.parent
    if not node.parent:
        return None
    node = node.parent[dir_]
    dir_opposite = 'right' if dir_ == 'left' else 'left'
    while not isinstance(node, Leaf):
        node = node[dir_opposite]
    return node


def explode(node: Node):
    assert node.parent
    zero_leaf = Leaf(value=0, parent=node.parent)
    for dir_ in ('left', 'right'):
        leaf = node[dir_]
        assert isinstance(leaf, Leaf)
        if near := inorder_near(leaf, dir_):
            near.value += leaf.value
        if node is node.parent[dir_]:
            node.parent[dir_] = zero_leaf


def split(leaf: Leaf, depth: int):
    assert leaf.parent
    dir_ = 'left' if leaf.parent.left == leaf else 'right'
    left = Leaf(leaf.value // 2)
    right = Leaf(ceil(leaf.value / 2))
    node = Node(left=left, right=right, parent=leaf.parent)
    left.parent = right.parent = leaf.parent[dir_] = node
    if depth == 4:
        explode(node)


def reduce(root: Node):
    for node, depth in inorder_walk(root):
        if depth == 4 and isinstance(node, Node):
            explode(node)
    while True:
        for x, depth in inorder_walk(root):
            if isinstance(x, Leaf) and x.value >= 10:
                split(x, depth)
                break
        else:  # nobreak
            break


def add(left: Node, right: Node):
    node = Node(left=left, right=right)
    left.parent = right.parent = node
    reduce(node)
    return node


def add_all(nodes: Iterable[Node]) -> Node:
    return functools.reduce(add, nodes)


def magnitude(node: TreeNode) -> int:
    if isinstance(node, Leaf):
        return node.value
    return 3 * magnitude(node.left) + 2 * magnitude(node.right)


def find_largest_pair_magnitude(s: str) -> int:
    max_magnitude = 0
    for a, b in permutations(s.splitlines(), r=2):
        m = magnitude(add(parse_tree(a), parse_tree(b)))
        max_magnitude = max(max_magnitude, m)
    return max_magnitude


def solve() -> tuple[int, int]:
    tree_str = read_puzzle()
    nodes = parse(tree_str)
    return magnitude(add_all(nodes)), find_largest_pair_magnitude(tree_str)


if __name__ == '__main__':
    print(solve())
