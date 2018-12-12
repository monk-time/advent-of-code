from dataclasses import dataclass, field
from itertools import chain
from typing import Iterable, List

from helpers import read_puzzle


def parse(s: str) -> List[int]:
    return [int(n) for n in s.split()]


def metadata_linear(nums: List[int]) -> List[int]:
    index, res = 2, []
    stack = [nums[:index]]
    while stack:
        meta = stack[-1][1]  # can be overwritten later
        if stack[-1][0]:  # at the start of the next child
            num_children, meta = nums[index:index + 2]
            index += 2
            if num_children:
                stack.append([num_children, meta])
                continue  # skip the final handling of metadata entries
            else:
                stack[-1][0] -= 1
        else:
            stack.pop()
            if stack:  # handle cascading ends of nodes
                stack[-1][0] -= 1
        res += nums[index:index + meta]
        index += meta
    return res


@dataclass
class Node:
    # end: Optional[int] = None
    children: List['Node'] = field(default_factory=list)
    meta: List[int] = field(default_factory=list)

    def __str__(self):
        meta_str = ' '.join(str(num) for num in self.meta)
        children_str = ' '.join(str(node) for node in self.children)
        if children_str:
            children_str += ' '
        return f'[{len(self.children)} {len(self.meta)} {children_str}({meta_str})]'


def build_tree(nums: List[int]):
    def parse_node(start):
        n_children, n_meta = nums[start:start + 2]
        root = Node()
        start += 2
        for _ in range(n_children):
            child = parse_node(start)
            root.children.append(child)
            start = child.end + 1
        root.end = start + n_meta - 1
        root.meta = nums[start:root.end + 1]
        return root

    return parse_node(0)


def metadata_rec(node: Node) -> Iterable[int]:
    yield from node.meta
    for child in node.children:
        yield from metadata_rec(child)


def metadata_as_indices(node: Node) -> Iterable[int]:
    if not node.children:
        yield sum(node.meta)
    else:
        refs = [node.children[i - 1] for i in node.meta if i <= len(node.children)]
        yield from chain(*map(metadata_as_indices, refs))


if __name__ == '__main__':
    tree = build_tree(parse(read_puzzle()))
    print(sum(metadata_rec(tree)), sum(metadata_as_indices(tree)))
