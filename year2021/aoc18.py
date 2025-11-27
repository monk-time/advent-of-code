# https://adventofcode.com/2021/day/18
# tags: #trees

import functools
from collections import UserList
from dataclasses import dataclass
from itertools import chain, permutations
from math import ceil
from typing import TYPE_CHECKING, cast

from utils_proxy import read_puzzle

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

MAX_DEPTH = 4


@dataclass
class Node[T]:
    value: T
    depth: int


class Tree(UserList[Node[int]]):
    def __str__(self) -> str:
        return collapse(self, lambda a, b: f'[{a},{b}]')

    __repr__ = __str__


def parse_tree(s: str) -> Tree:
    depth = 0
    tree = Tree()
    for ch in s:
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
        elif ch.isdigit():
            tree.append(Node(value=int(ch), depth=depth - 1))
    return tree


def parse(s: str) -> tuple[Tree, ...]:
    return tuple(parse_tree(line) for line in s.splitlines())


def collapse[T](tree: Tree, func: Callable[[T | int, T | int], T]) -> T:
    stack: list[Node[T] | Node[int]] = []
    for node in tree:
        stack.append(node)
        while len(stack) >= 2 and stack[-1].depth == stack[-2].depth:
            right, left = stack.pop(), stack.pop()
            collapsed = func(left.value, right.value)
            stack.append(Node(value=collapsed, depth=left.depth - 1))
    return cast('T', stack[0].value)


def explode(tree: Tree, i: int):
    if i > 0:
        tree[i - 1].value += tree[i].value
    if i + 2 < len(tree):
        tree[i + 2].value += tree[i + 1].value
    zero = Node(value=0, depth=MAX_DEPTH - 1)
    tree[i : i + 2] = [zero]


def split(tree: Tree, i: int):
    node = tree[i]
    depth = node.depth + 1
    a_val, b_val = node.value // 2, ceil(node.value / 2)
    if depth == MAX_DEPTH:
        if i > 0:
            tree[i - 1].value += a_val
        if i + 1 < len(tree):
            tree[i + 1].value += b_val
        node.value = 0
        return
    left = Node(value=a_val, depth=depth)
    right = Node(value=b_val, depth=depth)
    tree[i : i + 1] = [left, right]


def reduce(tree: Tree):
    i = 0
    while i < len(tree) - 1:
        if tree[i].depth == tree[i + 1].depth == MAX_DEPTH:
            explode(tree, i)
        i += 1
    while True:
        i = next((i for i, n in enumerate(tree) if n.value >= 10), None)
        if i is None:
            break
        split(tree, i)


def add(left: Tree, right: Tree) -> Tree:
    tree = Tree()
    for node in chain(left, right):
        tree.append(Node(value=node.value, depth=node.depth + 1))
    reduce(tree)
    return tree


def add_all(nodes: Iterable[Tree]) -> Tree:
    return functools.reduce(add, nodes)


def magnitude(tree: Tree) -> int:
    return collapse(tree, lambda a, b: 3 * a + 2 * b)


def find_largest_pair_magnitude(s: str) -> int:
    return max(
        magnitude(add(parse_tree(a), parse_tree(b)))
        for a, b in permutations(s.splitlines(), r=2)
    )


def solve() -> tuple[int, int]:
    tree_str = read_puzzle()
    nodes = parse(tree_str)
    return magnitude(add_all(nodes)), find_largest_pair_magnitude(tree_str)


if __name__ == '__main__':
    print(solve())
